# snapshotalyzer
Demo project to manage AWS EC2 instance snapshots.

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Prerequisite

* Clone this repository
`git clone https://github.com/hanantoprabowo/snapshotalyzer.git`
* Create an AWS account
* Create an IAM user, which has
  * a programmatical access (Access Key ID and Secret Access Key)
  * a *AmazonEC2FullAccess* policy
* Download and install [Anaconda](https://www.anaconda.com/download/)
* Start Anaconda Prompt
  * Install the required packages using [conda](https://www.anaconda.com/download/)
  `conda install -c conda-forge awscli`
  `conda install -c anaconda boto3`
  `conda install -c anaconda click`
  * Create an AWS CLI configuration file for the profile *shotty*
  `aws configure --profile shotty`
* Start one or two EC2 instance(s) (using AWS Console, CLI or SDK)

## Running

### List instances
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] instances list [--project=<project tag value>] [--instance=<instance ID>]
```

Examples:
```python
$ python shotty\python.py instances list
$ python shotty\python.py --profile=shotty instances list
$ python shotty\python.py --profile=shotty --region=eu-central-1 instances list
$ python shotty\python.py instances list --project=Valkyrie
$ python shotty\python.py instances list --instance=i-06c24bedf242f768f
```

### Start instances
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] instances start [--project=<project tag value>] [--instance=<instance ID>] [--force]
```

Notes:
* *--force* has to be provided if neither *--project* nor *--instance* is specified. The command will be applied to **ALL** instances.

Examples:
```python
$ python shotty\python.py instances start --force
$ python shotty\python.py --profile=shotty instances start --force
$ python shotty\python.py --profile=shotty --region=eu-central-1 instances start --force
$ python shotty\python.py instances start --project=Valkyrie
$ python shotty\python.py instances start --instance=i-06c24bedf242f768f
```

### Stop instances
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] instances stop [--project=<project tag value>] [--instance=<instance ID>] [--force]
```

Notes:
* *--force* has to be provided if neither *--project* nor *--instance* is specified. The command will be applied to **ALL** instances.

Examples:
```python
$ python shotty\python.py instances stop --force
$ python shotty\python.py --profile=shotty instances stop --force
$ python shotty\python.py --profile=shotty --region=eu-central-1 instances stop --force
$ python shotty\python.py instances stop --project=Valkyrie
$ python shotty\python.py instances stop --instance=i-06c24bedf242f768f
```

### Reboot instances
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] instances reboot [--project=<project tag value>] [--instance=<instance ID>] [--force]
```

Notes:
* *--force* has to be provided if neither *--project* nor *--instance* is specified. The command will be applied to **ALL** instances.

Examples:
```python
$ python shotty\python.py instances reboot --force
$ python shotty\python.py --profile=shotty instances reboot --force
$ python shotty\python.py --profile=shotty --region=eu-central-1 instances reboot --force
$ python shotty\python.py instances reboot --project=Valkyrie
$ python shotty\python.py instances reboot --instance=i-06c24bedf242f768f
```

### Create snapshots from instances
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] instances snapshot [--project=<project tag value>] [--instance=<instance ID>] [--force]
```

Notes:
* *--force* has to be provided if neither *--project* nor *--instance* is specified. The command will be applied to **ALL** instances.

Examples:
```python
$ python shotty\python.py instances snapshot --force
$ python shotty\python.py --profile=shotty instances snapshot --force
$ python shotty\python.py --profile=shotty --region=eu-central-1 instances snapshot --force
$ python shotty\python.py instances snapshot --project=Valkyrie
$ python shotty\python.py instances snapshot --instance=i-06c24bedf242f768f
```

### List volumes
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] volumes list [--project=<project tag value>] [--instance=<instance ID>]
```

Examples:
```python
$ python shotty\python.py volumes list
$ python shotty\python.py --profile=shotty volumes list
$ python shotty\python.py --profile=shotty --region=eu-central-1 volumes list
$ python shotty\python.py volumes list --project=Valkyrie
$ python shotty\python.py volumes list --instance=i-06c24bedf242f768f
```

### List snapshots
```python
$ python shotty\python.py [--profile=<profile>] [--region=<region>] snapshots list [--project=<project tag value>] [--instance=<instance ID>] [--all]
```

Notes:
* *--all* will show all snapshots. If it is not specified, only the latest snapshot will be shown.

Examples:
```python
$ python shotty\python.py snapshots list`
$ python shotty\python.py --profile=shotty snapshots list
$ python shotty\python.py --profile=shotty --region=eu-central-1 snapshots list
$ python shotty\python.py snapshots list --project=Valkyrie
$ python shotty\python.py snapshots list --instance=i-06c24bedf242f768f
$ python shotty\python.py snapshots list --all
```

## References

* [Original code (by Robin Norwood)](https://github.com/robin-acloud/snapshotalyzer-30000)
* [Project exercise (by Adam Schiestel)](https://acloud.guru/forums/python-for-beginners/discussion/-LVPUOO90Q6yEaDbIk1w/Completed%20all%209%20exercises)