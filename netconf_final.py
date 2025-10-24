from ncclient import manager
import xmltodict

def setup(ip):
    m = manager.connect(
        host=ip,
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
        )
    return m

def check_interface(ip):
    netconf_filter = """
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070200</name>
        </interface>
      </interfaces-state>
    </filter>
    """
    
    try:
        m = setup(ip)
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        interface_data = netconf_reply_dict.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {}).get("interface")

        if interface_data:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error in check_interface: {e}")
        return False

def create(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070200</name>
          <description>My NETCONF loopback</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            ianaift:softwareLoopback
          </type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>172.2.0.1</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    if check_interface(ip):
        return "Cannot create: Interface loopback 66070200"
    else:
        try:
            netconf_reply = netconf_edit_config(ip, netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 66070200 is created successfully using Netconf"
            else:
                return "Cannot create: Interface loopback 66070200"
        except:
            print("Error!")
            return "Cannot create: Interface loopback 66070200"


def delete(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
          <name>Loopback66070200</name>
        </interface>
      </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(ip, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070200 is deleted successfully using Netconf"
        else:
            return "Cannot delete: Interface loopback 66070200"
    except:
        print("Error!")
        return "Cannot delete: Interface loopback 66070200"


def enable(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070200</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(ip, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070200 is enabled successfully using Netconf"
        else:
            return "Cannot enable: Interface loopback 66070200"
    except:
        print("Error!")
        return "Cannot enable: Interface loopback 66070200"


def disable(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070200</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(ip, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070200 is shutdowned successfully using Netconf"
        else:
            return "Cannot shutdown: Interface loopback 66070200"
    except:
        print("Error!")
        return "Cannot shutdown: Interface loopback 66070200"

def netconf_edit_config(ip, netconf_config):
    m = setup(ip)
    return  m.edit_config(target="running", config=netconf_config)


def status(ip):
    netconf_filter = """
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070200</name>
        </interface>
      </interfaces-state>
    </filter>
    """

    m = setup(ip)
    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if netconf_reply_dict:
            interface_data = netconf_reply_dict.get("rpc-reply").get("data").get("interfaces-state").get("interface")
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = interface_data.get("admin-status")
            oper_status = interface_data.get("oper-status")
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070200 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070200 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070200 (checked by Netconf)"
    except:
       print("Error!")
