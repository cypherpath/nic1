# nic1 

nic1 (pronounced: "Nick One") is a command-line compiler for building a Software Defined Infrastructure (SDI) from the contents of both open and proprietary network capture/infrastructure data formats. Currently, only the libpcap format is supported but other data formats will be added as the project grows. nic1 stands for Network Infrastructure Compiler One. The purpose of nic1 is to parse existing and live network infrastructure formats and then generate an executable SDI which Cypherpath's SDI OS can run, making the compiled infrastructure definition format into a real operational infrastructure.

## Getting Started

To get started you will need to clone the nic1 repository, have API access to a Cypherpath SDI OS deployment, and have a pcap file of the network you would like to compile to an SDI. Cypherpath provides a free Community Edition of SDI OS with full API access. You can download the latest SDI OS Community Edition, license, and docs from Cypherpath's portal at https://my.cypherpath.com.

Before starting, please have all the prerequisites met (below).

Update SDIOS_CREDS in settings.py to have your SDI OS API account username and password along with API client_id, API client_secret. 
```
SDIOS_CREDS = {
  "username": "user",
  "password": "password",
  "client_id": "client",
  "client_secret": "secret"
}
```
DO NOT COMMIT settings.py to any repo with your specific credentials still in it. In the meantime, you could modify authorizer.py to load credentials from an environment variable or through an encryption algorithm. For now we leave this up to the end user, but bootstrap nic1 with the settings.py approach.

In settings.py you should also set the SDIOS_DOMAIN. This can be an IP address or domain name. SDIOS_VERIFY_SSL will skip the ssl verification when set to False. This supports SDI OS deployments with self-signed certificates.

It is helpful to validate your SDI OS API access/deployment setup using the curl command before runing nic1. See the SDI OS Restful API Guide for further details. This will ensure you have a functioning SDI OS system eliminating any issues with getting API access to it set up.

From the nic1 directory invoke the compiler, passing one or more space sperated pcaps with the -f or --files flag. You can also specify a directory of pcap files.

```
user@hostname nic1$ ./nic1.py -f ./Pathtopcaps

```
Once nic1 is complete it will display the the URL to your newly-created SDI or an error if something has failed.

```
user@hostname nic1$ ./nic1.py -f ../PCAP/SingleHTTP.pcap

nic1 has finished!  View your SDI at: https://www.mysdiosdomain.com/sdi/sdi_ID/topology_view/

```

Your SDI will power on but machines will not have disk images assigned. You can at this point attach disk images to the machines in the SDI. We are currently working towards automating this process so you can specify a catalog of machines to draw from. For more information or to collaborate on this feature please see the Roadmap for nic1. 


### System Dependencies

Below are the nic1 package requirements and installation commands for Arch Linux. Please see the packages websites for other operating systems' installation guides. 

python3
```
user@hostname ~$ sudo pacman -S python3
```

tshark is provided by wireshark-cli; there is no need to install the GUI.
```
user@hostname ~$ sudo pacman -S wireshark-cli
```


### Installing 

First, clone the repository via standard Git cloning to the directory of your choice. Example:
```
user@hostname ~$ git clone https://github.com/cypherpath/nic1.git
```
nic1 is now installed and ready to run if the prerequisites are installed as described above; however, nic1 will not run successfully without proper system configuration first. As described in the Getting Started section, the settings.py file will need changed to allow for proper access to your Cypherpath SDI OS deployment. 

We will use a virtualenv to install Python dependencies and keep things organized. Alternatively, you can directly install the requirements.txt into your system Python. If you don't have virtualenv you can install it with pip.

```
user@hostname nic1$ pip install virtualenv
```

Now let's use virtualenv to create a environment for our Python resources inside our root nic1 directory:
```
user@hostname nic1$ virtualenv venv
```

Now that we have a virtualenv we need to activate it:
```
user@hostname nic1$ source venv/bin/activate 
```

Next we can install the python dependencies for nic1 into the virtualenv:
```
user@hostname nic1$ pip install -r requirements.txt
```

After these changes, nic1 can now be run, producing a result similar to this:
```
user@hostname nic1$ ./nic1.py ./Pathtopcap

nic1 has finished! View your SDI at https://<client_info_domain>/sdi/<sdi_id>/topology_view
```

## Usage Guide 

nic1 can print out its help options by passing the help flag.
```
user@hostname nic1$ nic1.py -h 
```

nic1 is started by invoking it via the command-line and passing flags to it. To compile a pcap you use the -f or --files argument. This can be multiple space-separated files or a directory of pcap files.
```
user@hostname nic1$ nic1.py -f <PCAP_file(s)>
```

Note that nic1 requires that it be run from the root directory of the project. The required imports currently prevent it from running from any other directory.
nic1 requires pcap files to process. These are passed as the last arguments in the command line, as shown above. Alternatively, multiple files can be passed this way:
```
user@hostname nic1$ ./nic1.py -f PCAP_file_1.pcap PCAP_file_2.pcap
```

An entire directory can also be passed in. Note, however, that files which are not pcap files will cause errors in the compiler, printing them as output.
```
user@hostname nic1$ ./nic1.py -f ./directory_of_PCAPs
```

On success, nic1 will print a short message describing where to find the newly-generated SDI. The sdi_id is randomly created by Cypherpath SDI OS. The client_info_domain is always the third line in the client_info file.
```
nic1 has finished! View your SDI at https://<client_info_domain>/sdi/<sdi_id>/topology_view
```

By specifying the -a or --all flag before the -f PCAP files to parse or after the pcap list, nic1 will be verbose, printing out the entire state of the parser before generating the SDI. Information included involves packets, IPs, machines, networks, and VLANs, if any.

nic1 will print a short error message whenever it cannot connect to Cypherpath's API. These error messages also include the response number of the bad connection for diagnostic purposes. If these errors appear, there is a very good chance that the completed SDI will not accurately represent the network described by the PCAP file.

## Versioning 

The initial release of nic1 is version 0.5. The compiler's version number takes the form MAJOR.MINOR. We are marching towards a 1.0 version. To learn more about the future of the project please refer to the wiki roadmap.

## Contributing

We welcome all contributions to nic1, be that new features, data formats, bugfixes, extensions, tutorials, documentation, example applications, diagrams or pretty much anything else! If you have something you would like included in nic1, please create a pull request on github.

Before submitting bug fixes or feature requests please read CONTRIBUTING.md
