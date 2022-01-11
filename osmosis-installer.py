import subprocess
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def completeCosmovisor ():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The cosmovisor service is currently running in the background") 
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: sudo systemctl status cosmovisor")
    print(bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: journalctl -u cosmovisor -f"+ bcolors.ENDC)


def completeOsmosisd ():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!") 
    print(bcolors.OKGREEN + "The osmosisd service is currently running in the background") 
    print(bcolors.OKGREEN + "To see the status of the osmosis daemon, run the following command: sudo systemctl status osmosisd")
    print(bcolors.OKGREEN + "To see the live logs from the osmosis daemon, run the following command: journalctl -u osmosisd -f"+ bcolors.ENDC)


def cosmovisorInit ():
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes, install cosmovisor and set up background service
2) No, just set up an osmosisd background service 
    """)
    useCosmovisor = input(bcolors.OKGREEN + 'Enter Choice: ')
    if useCosmovisor == "1":
        print(bcolors.OKGREEN + "Setting Up Cosmovisor" + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/cosmos/cosmos-sdk"], shell=True)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/cosmos-sdk'))
        subprocess.run(["git checkout v0.44.0"], shell=True)
        subprocess.run(["make cosmovisor"], shell=True, env=my_env)
        subprocess.run(["cp cosmovisor/cosmovisor "+ GOPATH +"/bin/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/upgrades"], shell=True)
        subprocess.run(["echo '# Setup Cosmovisor' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_NAME=osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_HOME="+ HOME.stdout.strip()+"/.osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)    
        subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> "+ HOME.stdout.strip()+"/.profile"], shell=True) 
        subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True) 
        subprocess.run([". "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["cp "+ GOPATH +"/bin/osmosisd "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)     
        print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User="""+ USER.stdout.strip()+"""
ExecStart="""+ HOME.stdout.strip()+"""/go/bin/cosmovisor start
Restart=always
RestartSec=3
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
' >cosmovisor.service
        """], shell=True)
        subprocess.run(["sudo mv cosmovisor.service /lib/systemd/system/cosmovisor.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True)
        subprocess.run(["clear"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        print(bcolors.OKGREEN + "Creating Osmosisd Service" + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Osmosis Daemon
After=network-online.target
[Service]
User="""+ USER.stdout.strip()+"""
ExecStart="""+ HOME.stdout.strip()+"""/go/bin/osmosisd start
Restart=always
RestartSec=3
LimitNOFILE=4096
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
[Install]
WantedBy=multi-user.target
' >osmosisd.service
        """], shell=True)
        subprocess.run(["sudo mv osmosisd.service /lib/systemd/system/osmosisd.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["sudo systemctl start osmosisd"], shell=True)
        subprocess.run(["clear"], shell=True)
        completeOsmosisd() 
    else:
        subprocess.run(["clear"], shell=True)
        print ("Wrong selection, try again")
        cosmovisorInit()



def snapshotInstall ():
    print(bcolors.OKGREEN + "Downloading Decompression Packages" + bcolors.ENDC)
    subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"], shell=True)
    print(bcolors.OKGREEN + "Downloading Snapshot" + bcolors.ENDC)
    proc = subprocess.run(["curl https://quicksync.io/osmosis.json|jq -r '.[] |select(.file==\""+ fileName +"\")|select (.mirror==\""+ location +"\")|.url'"], capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(HOME.stdout.strip()+'/.osmosisd/'))
    subprocess.run(["wget -O - "+proc.stdout.strip()+" | lz4 -d | tar -xvf -"], shell=True)
    subprocess.run(["clear"], shell=True)
    cosmovisorInit()
 


def mainNetLocation ():
    global location
    print(bcolors.OKGREEN + """Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco
    """)
    nodeLocationAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if nodeLocationAns == "1":
        subprocess.run(["clear"], shell=True)
        location = "Netherlands"
        snapshotInstall()
    elif nodeLocationAns == "2":
        subprocess.run(["clear"], shell=True)
        location = "Singapore"
        snapshotInstall()
    elif nodeLocationAns == "3":
        subprocess.run(["clear"], shell=True)
        location = "SanFrancisco"
        snapshotInstall()      
    else:
        subprocess.run(["clear"], shell=True)
        print ("Wrong selection, try again")
        mainNetLocation()



def testnetSnapshotInstall ():
    print(bcolors.OKGREEN + "Downloading Decompression Packages" + bcolors.ENDC)
    subprocess.run(["sudo apt-get install wget liblz4-tool aria2 pixz -y"], shell=True)
    print(bcolors.OKGREEN + "Downloading Snapshot" + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME.stdout.strip()+'/.osmosisd'))
    subprocess.run(["wget https://mp20.net/snapshots/osmosis-testnet/osmosis-testnet-mp20-latest.tar.xz"], shell=True)
    subprocess.run(["tar -I'pixz' -xvf osmosis-testnet-mp20-latest.tar.xz --strip-components=4"], shell=True)
    subprocess.run(["rm osmosis-testnet-mp20-latest.tar.xz"], shell=True)
    subprocess.run(["clear"], shell=True)
    cosmovisorInit()





def testnetType ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot (recommended)
2) I have my own Osmosis snapshot, skip to setting up cosmovisor and/or osmosisd service
3) Use statesync (NOT YET IMPLEMENTED)
    """) 
    dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        testnetSnapshotInstall()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        cosmovisorInit()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        print("Not yet implemented, try again later")
        testnetType()
    else:
        subprocess.run(["clear"], shell=True)
        print ("Wrong selection, try again")
        testnetType()


def mainNetType ():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned
2) Default
3) Archive
    """)

    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-pruned"
        mainNetLocation()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-default"
        mainNetLocation()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-archive"
        location = "Netherlands"
        snapshotInstall()       
    else:
        subprocess.run(["clear"], shell=True)
        print ("Wrong selection, try again")
        mainNetType()


def dataSyncSelection ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) I have my own Osmosis snapshot, skip to setting up cosmovisor and/or osmosisd service
3) Use statesync (NOT YET IMPLEMENTED)
    """) 
    dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        mainNetType()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        cosmovisorInit()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        print("Not yet implemented, try again later")
        dataSyncSelection()
    else:
        subprocess.run(["clear"], shell=True)
        print ("Wrong selection, try again")
        dataSyncSelection()



def setupMainnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    subprocess.run(["osmosisd init " + nodeName + " -o"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis" + bcolors.ENDC)
    subprocess.run(["wget -O "+ HOME.stdout.strip()+"/.osmosisd/config/genesis.json https://github.com/osmosis-labs/networks/raw/main/osmosis-1/genesis.json"], shell=True)
    subprocess.run(["clear"], shell=True)
    dataSyncSelection()


def setupTestnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmosis-testnet-0 -o"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis" + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME.stdout.strip()+'/.osmosisd/config'))
    subprocess.run(["wget https://github.com/osmosis-labs/networks/raw/unity/v4/osmosis-1/upgrades/v4/testnet/genesis.tar.bz2"], shell=True)
    print(bcolors.OKGREEN + "Finding and Replacing Seeds" + bcolors.ENDC)
    subprocess.run(["tar -xjf genesis.tar.bz2"], shell=True)
    subprocess.run(["rm genesis.tar.bz2"], shell=True)
    subprocess.run(["sed -i.bak -E 's/seeds = \"63aba59a7da5197c0fbcdc13e760d7561791dca8@162.55.132.230:2000,f515a8599b40f0e84dfad935ba414674ab11a668@osmosis.blockpane.com:26656\"/seeds = \"4eaed17781cd948149098d55f80a28232a365236@testmosis.blockpane.com:26656\"/g' ~/.osmosisd/config/config.toml"], shell=True)
    #subprocess.run(["osmosisd unsafe-reset-all"], shell=True)
    subprocess.run(["clear"], shell=True)
    testnetType()


def initNodeName():
    global nodeName
    nodeName= input(bcolors.OKGREEN + "Input desired node name (no quotes, cant be blank): ")    
    if nodeName and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        setupMainnet()
    elif nodeName and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        setupTestnet()
    else:
        subprocess.run(["Please insert a non-blank node name"], shell=True)
        initNodeName()



def initSetup ():
    global my_env
    print(bcolors.OKGREEN + "Updating Packages" + bcolors.ENDC)
    subprocess.run(["sudo apt-get update && sudo apt-get upgrade -y"], shell=True)
    print(bcolors.OKGREEN + "Installing Make and GCC" + bcolors.ENDC)
    subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"], shell=True)
    print(bcolors.OKGREEN + "Installing Go" + bcolors.ENDC)
    subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.17.2"], shell=True)
    print(bcolors.OKGREEN + "Reloading Profile" + bcolors.ENDC)    
    subprocess.run([". "+ HOME.stdout.strip()+"/.profile"], shell=True)
    print(bcolors.OKGREEN + "Installing Osmosis V6 Binary" + bcolors.ENDC) 
    os.chdir(os.path.expanduser(HOME.stdout.strip()))
    subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], shell=True)
    os.chdir(os.path.expanduser(HOME.stdout.strip()+'/osmosis'))
    subprocess.run(["git checkout v6.0.0"], shell=True)
    my_env = os.environ.copy()
    my_env["PATH"] = "/root/go/bin:/root/go/bin:/root/.go/bin:" + my_env["PATH"]
    subprocess.run(["make install"], shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    initNodeName()




def start ():
    subprocess.run(["clear"], shell=True)
    global HOME
    global USER
    global networkAns
    global GOPATH
    HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True)
    USER = subprocess.run(["echo $USER"], capture_output=True, shell=True, text=True)
    GOPATH = HOME.stdout.strip()+"/go"
    print(bcolors.OKGREEN + """
 ██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝                          


Welcome to the Osmosis node installer V1.0.0!
For more information, please visit docs.osmosis.zone

Please choose a network to join:
1) Mainnet (osmosis-1)
2) Testnet (osmosis-testnet-0)
    """)

    networkAns = input(bcolors.OKGREEN + 'Enter Choice: ')

    if networkAns == '1':
        subprocess.run(["clear"], shell=True)
        initSetup()
    elif networkAns == '2':
        subprocess.run(["clear"], shell=True)
        initSetup()
    else:
        print("Please only enter the number preceding the option and nothing else, in this case 1 or 2")
        start()


start()
