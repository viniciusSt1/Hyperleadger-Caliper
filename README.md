
# Scenario tests

## Install the Caliper NVM 
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash 

nvm install 18

```

## Install the Caliper NPM Package
```
npm install --only=prod @hyperledger/caliper-cli@0.5.0
```
## Check if it is installed correctly.
```
npx caliper --version
```
## Bind it to the latest version of Besu.
```
npx caliper bind --caliper-bind-sut besu:latest
```
## [OPTIONAL, THIS VERSION DO NOT NEED] Clone the caliper-benchmarks repository. This repository comes with some predefined Workloads against which you can run benchmarks.
```
git clone https://github.com/hyperledger/caliper-benchmarks.git
```
## Inside this `NetworkConfig` File, we want it to point towards the Web Socket URL, where our Besu Network is running. For this example, it is pointing to,  `ws://localhost:8546`. Also, the ABI for the smart contract has been left out from here, this can be added inside the `abi` field.
```
{
    "caliper": {
        "blockchain": "ethereum",
        "command" : {}
    },
    "ethereum": {
        "url": "ws://IP_BESU_NETWORK:8546",
        "fromAddress": "CARTEIRA PUBLICA ADM",
        "fromAddressPrivateKey": "CHAVE PRIVADA ADM",
        "transactionConfirmationBlocks": 10,
        "contracts": {
            "RevocationRegistry": {
                "address": "0x... ENDEREÇO DO CONTRATO",
                "estimateGas": true,
                "gas": {
                    "_revocation_": 800000
                },
                "abi":
[
ABI DO CONTRATO
]
            }
        }
    }
}
```
## Modify the config file for variation tests.
```
simpleArgs: &simple-args
  schema: ["did:indy2:indy_besu:MRDxoJ2Mz3WuyqaqsjVTdN/anoncreds/v0/SCHEMA/BasicIdentity/1.0.0","did:indy2:indy_besu:MRDxoJ2Mz3WuyqaqsjVTdN", "BasicIdentity","1.0.0", ["First Name","Last Name"]]
  numberOfAccounts: &number-of-accounts 100

test:
  name: CreateSchema Test
  description: >-
    This is an example benchmark for Caliper, to test the backend DLT's
    performance with simple account opening & querying transactions.
  workers:
    number: 1
  rounds:
    - label: CreateSchema
      description: >-
        Test description for the opening of an account through the deployed
        contract.
      txNumber: *number-of-accounts
      rateControl:
        type: fixed-rate
        opts:
          tps: 10
      workload:
        module: benchmarks/scenario/SchemaRegistry/createSchema.js
        arguments: *simple-args

monitors:
  resource:
  - module: docker
    options:
      interval: 5
      containers:
      - rpcnode
      - indy-besu-validator1-1
      - indy-besu-validator2-1
      - indy-besu-validator3-1
      - indy-besu-validator4-1
      - indy-besu-validator5-1
      charting:
        bar:
          metrics: [Memory(avg), CPU%(avg)]
        polar:
          metrics: [all]

observer:
  type: local
  interval: 5
```
## Running the final command!
```
npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario-marketplace-descentralized/Telecoin/config.yaml --caliper-networkconfig ./networks/besu/networkconfig.json --caliper-bind-sut besu:latest --caliper-flow-skip-install

npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario/ServiceContract/config.yaml --caliper-networkconfig config.json --caliper-bind-sut besu:latest --caliper-flow-skip-install


```


## NEW!

Install Dependencies 


configure run_test_local.py 

python3 run_test_local.py


npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario-monitoring/NodeHealthMonitor/config-reportStatus.yaml --caliper-networkconfig ./networks/besu/networkconfig.json --caliper-bind-sut besu:latest --caliper-flow-skip-install

npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario-monitoring/NodeHealthMonitor/config-reportStatus.yaml --caliper-networkconfig ./networks/besu-brad/networkconfig.json --caliper-bind-sut besu:latest --caliper-flow-skip-install


npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario-monitoring/NodeHealthMonitor/config-statusReports.yaml --caliper-networkconfig ./networks/besu-brad/networkconfig.json --caliper-bind-sut besu:latest --caliper-flow-skip-install

npx caliper launch manager  --caliper-workspace ./ --caliper-benchconfig benchmarks/scenario-monitoring/NodeHealthMonitor/config-getLatestStatus.yaml --caliper-networkconfig ./networks/besu-brad/networkconfig.json --caliper-bind-sut besu:latest --caliper-flow-skip-install

