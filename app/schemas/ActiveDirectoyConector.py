from ldap3 import Server, Connection, ALL, NTLM, SUBTREE, MODIFY_REPLACE 
from ldap3.extend import MicrosoftExtendedOperations
import os
from tools.logging import logger
from typing import List

ATTRIBUTES = ['cn', 'distinguishedName', 'sAMAccountName', 'mail', 'telephoneNumber', 'memberOf']

if os.getenv('LDAP_SERVER', False):
    LDAP_SERVER = os.getenv('LDAP_SERVER')
else:
    logger.debug('ENV LDAP_SERVER NOT FOUND')

if os.getenv('LDAP_USER_DN', False):
    LDAP_USER_DN = os.getenv('LDAP_USER_DN')
else:
    logger.debug('ENV LDAP_USER_DN NOT FOUND')

if os.getenv('LDAP_USER_DN_PASSWORD', False):
    LDAP_USER_DN_PASSWORD = os.getenv('LDAP_USER_DN_PASSWORD')
else:
    logger.debug('ENV LDAP_USER_DN_PASSWORD NOT FOUND')

class ActiveDirectoryConector(object):
    """Clase de coneccion de ldap para HNAP
    """

    _server = Server(LDAP_SERVER, get_info=ALL, use_ssl=True)
    _service_user_dn = 'CN=' + LDAP_USER_DN + ',OU=Application,OU=Users Accounts,DC=local,DC=hospitalposadas,DC=gob,DC=ar'
    _service_password = LDAP_USER_DN_PASSWORD

    def __init__(self) -> None:
        super().__init__()
        self._conn = Connection(self._server, user=self._service_user_dn, 
                                 password=self._service_password)

    def get_user_dn(self, samaccountname) -> str:
        """ Función para obtener el DN completo usando sAMAccountName
        Args:
            samaccountname (str): samaccountname

        Returns:
            str: Ruta completa
        """
    
        user_dn = None
        search_base = 'DC=local,DC=hospitalposadas,DC=gob,DC=ar'
        search_filter = f'(sAMAccountName={samaccountname})'
        self._conn.bind()
        self._conn.search(search_base, search_filter, search_scope=SUBTREE, attributes=['distinguishedName'])
        if self._conn.entries:
            user_dn = self._conn.entries[0].distinguishedName.value
        self._conn.unbind()
        return user_dn

    # Función para autenticar usuario
    def authenticate(self, username, password):
        """Función para autenticar usuario

        Args:
            username (str): samaccountname
            password (str): password

        Returns:
            bool: True si el login es correcto, False si no lo es
        """
        try:
            user_dn = self.get_user_dn(username)
            if not user_dn:
                return False

            # Crear conexión al servidor LDAP con las credenciales del usuario
            user_conn = Connection(self._server, user=user_dn, password=password)

            # Intento de conexión y autenticación
            if not user_conn.bind():
                return False
            else:
                self.ou = user_conn.user
                return True

        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

    def search_user(self, username: str, attributes=ATTRIBUTES):
        """Busca un usuario por samaccountname, y devuelve un diccionario 
        con los attributos ingresados, 
        por defecto son ['cn', 'distinguishedName', 'sAMAccountName', 'mail', 'telephoneNumber', 'memberOf']

        Args:
            username (str): samaccountname
            attributes (list[str], optional): lista de attr. Defaults to ATTRIBUTES.

        Returns:
            dict: {'attr':data}
        """

        try:
            res = {}
            user_dn = self.get_user_dn(username)

            # Realizar una búsqueda en el subárbol de la OU especificada
            self._conn.bind()
            self._conn.search(
                search_base=user_dn,
                search_filter='(objectClass=user)',
                attributes=ATTRIBUTES
            )
            
            # Recorrer y mostrar los resultados
            for entry in self._conn.entries:
                for att in ATTRIBUTES:
                    res.update({att: str(getattr(entry, att, '' ))})
            self._conn.unbind()
            
            return res
        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

    def get_users_group(self, name) -> list:
        """Devuelve los usuarios del grupo

        Args:
            name ( str ): Nombre del grupo

        Returns:
            list: List[str]
        """
        res = []
        try:
            search_filter = '(&(objectClass=group)(cn={gn}))'.format(gn=name)

            # Realizar una búsqueda en el subárbol de la OU especificada
            self._conn.bind()
            self._conn.search(
                search_base='DC=local,DC=hospitalposadas,DC=gob,DC=ar',
                search_filter=search_filter,
                attributes=['member']
            )            
            # Recorrer y mostrar los resultados
            for entry in self._conn.entries:
                for member in entry.member:
                    res.append(member)
            

        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

        finally:
            self._conn.unbind()

        return res
    
    def get_pcs(self, name:str = None) -> list:
        """Devolucion de CN de las pc

        Returns:
            list: List[str]
        """
        ATTRIBUTES = ['distinguishedName', 'CN', 'description']
        res = []
        try:
            if name:
                search_filter = '(&(objectClass=computer)(cn={gn}*))'.format(gn=name)
            else:
                search_filter = '(objectClass=computer)'
            # Realizar una búsqueda en el subárbol de la OU especificada
            self._conn.bind()
            self._conn.search(
                search_base='OU=Computers Accounts,DC=local,DC=hospitalposadas,DC=gob,DC=ar',
                search_filter=search_filter,
                attributes=ATTRIBUTES
            )
            # Recorrer y mostrar los resultados
            for entry in self._conn.entries:
                d = {}
                for ATTRIBUTE in ATTRIBUTES:
                    d[ATTRIBUTE] = str(getattr(entry, ATTRIBUTE, ''))
                res.append(d)

        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

        finally:
            self._conn.unbind()

        return res

    def set_attributes(self, username: str, atts: dict)-> bool :
        """Actualiza informaicon del usuario

        Args:
            username (str): samacountname
            atts (dict): diccionario con los attributos a actualizar

        Returns:
            bool: True si actualizo False si no
        """
        try:
            res = {}
            user_dn = self.get_user_dn(username)
            self._conn.bind()
            for att in atts.keys():
                res[att] = [(MODIFY_REPLACE, [atts[att]])]
            res = self._conn.modify(user_dn, res)
        except Exception as e:
                    logger.debug('Exception:', str(e))
                    return False

        finally:
            self._conn.unbind()
            if res:
                return True
            return False
        
    def set_pass(self, username:str, password:str) -> bool :
        try:
            # username = '22807349'
            res = {}
            user_dn = self.get_user_dn(username)
            self._conn.bind()
            microsoft = MicrosoftExtendedOperations(self._conn)
            res = microsoft.modify_password(user=user_dn, new_password=password)
        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

        finally:
            self._conn.unbind()
            if res:
                return True
            return False


    def delPV(self, name: str) -> bool:
        try:
            # Datos del usuario al que se le reseteará la contraseña
            target_user_dn = 'CN={name},OU=Desktop,OU=Computers Accounts,DC=local,DC=hospitalposadas,DC=gob,DC=ar'.format(name=name)

            # Crear conexión
            # server = Server('ldaps://local.hospitalposadas.gob.ar:636', get_info=ALL, use_ssl=True)
            # conn = Connection(server, service_user_dn, service_password, auto_bind=True)
            self._conn.bind()
            # Resetear la contraseña
            # res = conn.modify(target_user_dn, {'CN': [(MODIFY_REPLACE, ['WIN-0010'])]})
            res = self._conn.delete(target_user_dn)

        except Exception as e:
            logger.debug('Exception:', str(e))
            return False

        finally:
            self._conn.unbind()
            if res:
                return True
            return False

