*** Settings ***
Documentation   SSH Connection Test
Library         SSHLibrary
Library         Collections
Library         re
Variables       benchmark_vm_accessor.py


*** Test Cases ***
Connect and Test SSH Connection with Key
    [Documentation]    Test SSH connection using a key.
    [Tags]    ssh    key
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    Log    Connection with key test completed.

Execute Script with SSH Key Connection
    [Documentation]    Execute a script on the remote server using SSH key.
    [Tags]    ssh    execute
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${output}=    Execute Command    ${COMMAND_SCRIPT_1}
    Run Keyword And Continue On Failure    Log Many    {{{${output}}}    level=INFO
    Run Keyword And Continue On Failure    Should Be Empty    ${output}    msg=Script execution failed
    Log    Script execution test completed.

Test CPU Performance
    [Documentation]    Test CPU performance on a remote server.
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    ${cpu_usage}=    Execute Command    top -bn1 | grep "Cpu(s)" | awk '{print $2}'
    Log    CPU Usage on Remote Server: ${cpu_usage}
    Close Connection
    Run Keyword If    ${cpu_usage} > 90    Fail    CPU usage is high
    ...    ELSE    Log    CPU usage is within acceptable limits

Service Monitoring
    [Documentation]    Ensure critical services like web servers are running.
    [Tags]    service    monitoring
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${status}=    Execute Command    systemctl status apache2
    Run Keyword And Continue On Failure    Log Many    {{{${status}}}    level=INFO
    Should Not Contain    ${status}    inactive    msg=Apache2 service is inactive

Log Monitoring Test
    [Documentation]    Check for errors in the system log file.
    [Tags]    logs    monitoring
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${error_count}=    Execute Command    grep -c 'error' /var/log/syslog | awk '{print $1}'
    ${error_count_as_integer}=    Convert To Integer    ${error_count}
    Log    Number of errors in syslog: ${error_count_as_integer}
    ${syslog_errors}=    Execute Command    grep 'error' /var/log/syslog
    Run Keyword If    ${error_count_as_integer} > 0    BuiltIn.Log    ${syslog_errors}

Security Checks Test
    [Documentation]    Verify firewall status and security configurations.
    [Tags]    security    checks
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${firewall_status}=    Execute Command    ufw status
    Run Keyword And Continue On Failure    Log Many    {{{${firewall_status}}}    level=INFO
    Should Not Contain    ${firewall_status}    inactive    msg=Firewall is not active

Network Connectivity Test
    [Documentation]    Test network connectivity to a specific service.
    [Tags]    network    connectivity
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${ping_result}=    Execute Command    ping -c 4 google.com
    Log Many    {{{${ping_result}}}    level=INFO
    Should Contain    ${ping_result}    0% packet loss    msg=Network connectivity issue

Performance Monitoring Test
    [Documentation]    Monitor system performance metrics.
    [Tags]    performance    monitoring
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${performance_metrics}=    Execute Command    top -bn1
    Log Many    {{{${performance_metrics}}}    level=INFO

Automated Deployment Test
    [Documentation]    Check status of an automated deployment tool.
    [Tags]    deployment    automated
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${deployment_status}=    Execute Command    ansible-playbook --check your_playbook.yml
    Log Many    {{{${deployment_status}}}    level=INFO

Backup and Recovery Test
    [Documentation]    Verify backup processes and test recovery procedures.
    [Tags]    backup    recovery
    Open Connection    ${HOST}    port=${PORT}
    Login With Public Key    ${USERNAME}    ${KEY_FILE}
    [Teardown]    Close Connection
    ${backup_test}=    Execute Command    rsync --dry-run -av /source /backup
    Log Many    {{{${backup_test}}}    level=INFO

