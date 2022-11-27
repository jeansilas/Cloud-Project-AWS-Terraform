import json
import resource
import sys
import time
import os
import boto3
import pickle

class Cloud:

    def __init__(self):
        self.variables : str = "variables.json"
        try:
            self.archive_name : str = sys.argv[1]
        except:
            self.archive_name : str = "main.tf"

        # default
        self.terraform = '''terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}'''
        self.provider = '''provider "aws" {
  region  = "~region~"
}'''

        self.resource = '''resource "aws_instance" "~name~" {
  ami           = "~ami~"
  instance_type = "~instance~"
  subnet_id = "${aws_subnet.public.id}"
  vpc_security_group_ids = [aws_security_group.~rule~.id]

  tags = {
    Name = "~tag~"
  }
}'''

        self.user = '''resource "aws_iam_user" "~userlb~" {
  name = "~user~"
  path = "/system/"

  tags = {
    tag-key = "~tag-user~"
  }
}'''    
        self.vpc = '''resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
   tags = {
    Name = "~vpc~"
  }
}'''
        self.group_security = '''resource "aws_security_group" "~group_security_name~" {
  name        = "~group_security_name~"

  vpc_id = aws_vpc.main.id

  ingress {
    from_port        = ~from_port~
    to_port          = ~to_port~
    protocol         = "~protocol~"
    cidr_blocks      = ["10.0.0.0/24"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "~group_security_name~"
  }
}'''


        self.subnet = '''resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = "true" 
  availability_zone = "~region~a"

  tags = {
    Name = "~subnet~-public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  map_public_ip_on_launch = "true"
  availability_zone = "~region~b" 
  
  tags = {
    Name = "~subnet~-private"
  }
}
'''
        self.default_sg = '''resource "aws_security_group" "padrao" {
  name        = "padrao"

  vpc_id = aws_vpc.main.id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "padrao"
  }
}'''

        # Para listar
        self.states : int = 0
        self.regions : list(str) = None
        self.instances: list(str) = None
        self.amis: dict(str,str) = None

        # Inicializa as veriáveis do Json
        self.read_variables()

        # Para escolher
        self.name : str = None
        self.tag : str = None
        self.region : str = None
        self.instance : str = None
        self.ami: str = None

        #Rotinas
        self.routines = ["Listar os recursos","Criar Recursos","Criar Usuários","Excluir Recursos","Subir a Infraestrutura","Fechar Programa"]

        #Listagens
        self.lists = ["Usuários","Instâncias","Regiões","Grupos de Segurança"]

        #Recursos a serem criados:
        self.resources_type = ["Instâncias","Grupos de Segurança"]

        self.subnet_name :str = None 
        self.vpc_name    :str = None
        self.rule       :str = "default"


        self.rewrite = 0
    
    def write_cache(self,archive:str,object, path=""):

        if path == "":
            path_ = ""
        else:
            path_= path+"/"
        
        with open(f"{path_}{archive}",'wb') as archive_:
            pickle.dump(object, archive_)

    def read_cache(self,archive:str,path=""):
        if path == "":
            path_ = ""
        else:
            path_= path+"/"
        with open(f"{path_}{archive}",'rb') as archive_:
            object_ = pickle.load(archive_)

        return object_
    
    def destroy_main(self):

        with open("main.tf","w") as file:
            file.write("")
    
    def update_archive_name(self):
        self.archive_name : str = self.region+"/main.tf"
    
    def read_variables(self):
        with open(self.variables, 'r', encoding='utf-8') as archive:
            variables = json.load(archive)
        self.regions = variables['region']
        self.instances = variables['tipo-instancia']
        self.amis = variables['ami']

    def format_choice(self,choices, ami = False):
        if ami:
            choices = [obj[0] for obj in choices]
        build_options_choices = zip(range(1,len(choices)+1),choices)
        options_message_med = "\n".join([f"    {obj[0]}.       {obj[1]}"  for obj in build_options_choices])
        options_message = f'''\nDigite o número que pareia com a opção que você deseja:\n\n\n'''+options_message_med+"\n\n\n"
        return options_message


    def choose_resource(self, i=""):
        errou = True
        # Escolhendo o nome da instância

        self.name = input(f"\nDigite o nome da instância:        default:[Instancia{i}.] \n")
        if self.name == "":
            self.name = f"Instancia{i}"

        # Escolhendo a tag da instância
        self.tag = input (f"\nDigite a tag a qual essa instância estará pareada:         default:[Tag{i}.] \n")
        if self.tag == "":
            self.tag = f"Tag{i}"

        # Escolhendo o tipo de instância
        while errou:
            try:
                self.instance = self.instances[self.region][int(input("\nEscolha o Tipo de instância     default:[1.]\n"+self.format_choice(self.instances[self.region])))-1]
                errou = False
            except:
                print("\n\n Algo deu errado. Tente escolher novamente\n\n")
                time.sleep(1)

        errou = True
        # Escolhendo a AMI da máquina (Imagem)
        while errou:
            try:
                self.ami = self.amis[self.region][int(input("\nEscolha a Imagem da instância    default:[1.]\n"+self.format_choice(self.amis[self.region],ami=True)))-1][1]
                errou = False
            except:
                 print("\n\n Algo deu errado. Tente escolher novamente\n\n")
                 time.sleep(1)
        
        if input('''\n\nQuer associar essa instância a alguma Grupo de Segurança ? ( digite "sim" ou "não"): ''') == "sim":
            try:
                list_sg_read = self.read_cache("sg",path=self.region)
                list_sg_read.append("padrao")
            except:
                list_sg_read = ["padrao"]
            self.rule = list_sg_read[int(input("\nEscolha o Grupo de Segurança\n"+self.format_choice(list_sg_read)))-1]
        else:
            self.rule = "padrao"
             

    
    def format_resource(self,resource:str,dict_resource = None, rewrite = False):
        if dict_resource is None:
            pass
        else:
            for text in dict_resource:
                resource = resource.replace(text[0],text[1])
        
        if rewrite:
            with open(self.archive_name,'w', encoding="utf-8") as archive:
                archive.write(resource+"\n\n\n")

        else:
            with open(self.archive_name,'a', encoding="utf-8") as archive:
                archive.write(resource+"\n\n\n")


    def build_instances(self):

        n = int(input("\nQuantas instâncias você quer criar: "))     # numbers of instances to be created
        i = 0                                                   # count of instances created
        while i < n :
            print(f"\n\nInstância {i+1:}\n\n")
            self.choose_resource(i=i)
            resource_dict = [("~name~",self.name),("~ami~",self.ami),("~instance~",self.instance),("~tag~",self.tag),("~rule~",self.rule)]
            self.format_resource(self.resource,dict_resource=resource_dict)
            i += 1
        print("\n\n\n\n\n[Infraestrutura Definida]\n\n\n")
    
    def build_users(self):
        self.format_resource(self.terraform,rewrite=True)
        self.format_resource('''provider "aws" {
  region  = "us-east-1"
}''')   
        users_list = []
        n = int(input("\nQuantos usuários você quer criar: "))     # numbers of user to be created
        i = 0                                                   # count of users created
        while i < n :
            print(f"\n\nUsuário {i+1:}\n\n")
            username = input("\n\nNome do usuário: ")
            users_list.append(username)
            user_dict = [("~user~",username),("~tag-user~",input("\n\nTag do usuário: \n\n")),("~userlb~",username)]
            self.format_resource(self.user,dict_resource=user_dict)
            i += 1
        self.write_cache("users",users_list,path="")
    
    def build_security_groups(self):

        list_sg = []

        n = int(input("\nQuantos Grupos de seguranca você quer criar: "))     # numbers of security groups to be created
        i = 0                                                                 # count of security groups created
        while i < n :
            print(f"\n\nGrupo de Segurança {i+1:}\n\n")
            security_group_name = input("\n\nNome do Grupo de Segurança: ")
            list_sg.append(security_group_name)
            from_port = input("\n\nPorta de Entrada(ingresso): ")
            to_port = input("\n\nPorta de Saida(ingresso): ")
            protocol = "tcp"
            gs_dict = [("~group_security_name~",security_group_name),("~from_port~",from_port),("~to_port~",to_port),("~protocol~",protocol)]
            self.format_resource(self.group_security,dict_resource=gs_dict)
            i += 1
        
        self.write_cache("sg",list_sg,path=self.region)
        

    def interface_routines(self):


        using = True

        while using:

            routines_options = self.format_choice(self.routines)

            errou = True
            while errou:
                try:
                    self.state = int(input(routines_options))
                    errou = False
                except:
                    print("\n\n Algo deu errado. Tente escolher novamente\n\n")
                    time.sleep(1)
            
            if (self.state == 1):
                errou = True
                while errou:
                    try:
                        choice_list = int(input(self.format_choice(self.lists)))
                        errou = False
                    except:
                        print("\n\n Algo deu errado. Tente escolher novamente\n\n")
                    time.sleep(1)

                if (choice_list == 1):
                    try:
                        users_iam = self.read_cache("users",path="users")
                    except:
                        users_iam = []
                    print("Os usuários da IAM são:")
                    for i in range(1,len(users_iam)+1):
                        print(f"{i}.   {users_iam[i-1]}")
                    
                    
                    
                    print("\n\n\n")
                    _ = input("Pressione enter para continuar. ")

                elif (choice_list == 2):
                    print("\n\n\n")
                    print("Região: us-east-1\n")
                    ec2 = boto3.resource('ec2',"us-east-1")
                    for instance in ec2.instances.all():
                        print(
                            "Tag: {0}\nId: {1}\nPlatform: {2}\nType: {3}\nPublic IPv4: {4}\nAMI: {5}\nState: {6}\n".format(
                            instance.tags[0]["Value"], instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state
                            )
                        )
                    print("\n")
                    print("\n\n\n")
                    print("Região: us-east-2\n")
                    ec2 = boto3.resource('ec2',"us-east-2")
                    for instance in ec2.instances.all():
                        print(
                            "Tag: {0}\nId: {1}\nPlatform: {2}\nType: {3}\nPublic IPv4: {4}\nAMI: {5}\nState: {6}\n".format(
                            instance.tags[0]["Value"], instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state
                            )
                        )
                    print("\n")
                    _ = input("Pressione enter para continuar. ")
                elif (choice_list == 3):
                    print("\n\n\nRegiões:\n us-east-1\n us-east-2\n")
                elif (choice_list == 4):
                    self.region = "us-east-1"
                    try:
                        sg_1  = self.read_cache("sg",path=self.region)
                    except:
                        sg_1 = []
                    self.region = "us-east-2"
                    try:
                        sg_2  = self.read_cache("sg",path=self.region)
                    except:
                        sg_2 = []
                    sg_1.append("padrao")
                    sg_2.append("padrao")
                    print("\nGrupos de Segurança da Regiao: us-east-1\n\n")
                    for i in range(1,len(sg_1)+1):
                        print(f"{i}.   {sg_1[i-1]}")
                    print("\nGrupos de Segurança da Regiao: us-east-2\n\n")
                    for i in range(1,len(sg_2)+1):
                        print(f"{i}.   {sg_2[i-1]}")


            elif (self.state == 2) :

                self.rewrite = int(input("Caso queira recomeçar uma nova estrutura, digite '1' caso contrário digite '0'.\n\nOBS: caso tenha acabado de adicionar a regras de Segurança, digite '0'. E caso mude a região, digite '1'\n : "))
            

            # Escolhendo a Região
                self.region = self.regions[int(input("\nEscolha a Região\n"+self.format_choice(self.regions)))-1]
                self.update_archive_name()

            # Escrevendo o terraform
                if self.rewrite:
                    self.format_resource(self.terraform,rewrite=True)
            
                # Escrevendo o provider
                    provider_dict = [("~region~",self.region)]
                    self.format_resource(self.provider,dict_resource=provider_dict)
                
                # Escolhendo a VPC
                    self.vpc_name = input("\n\n Nome de VPC: \n\n")

                
                # Escrevendo a VPC
                    vpc_dict = [("~vpc~",self.vpc_name)]
                    self.format_resource(self.vpc,dict_resource=vpc_dict)
                

                # Escolhendo a Subnet
                    self.subnet_name = input("\n\n Nome de Subnet: \n\n")

                # Escrevendo a Subnet
                    subnet_dict = [("~subnet~",self.subnet_name),("~region~",self.region)]
                    self.format_resource(self.subnet,dict_resource=subnet_dict)
                
                # Escrevendo um Grupo de Segurança
                    self.format_resource(self.default_sg)

                    self.write_cache("info",{"subnet":self.subnet_name,"vpc":self.vpc_name},path=self.region)  
                else:
                    self.vpc_name,self.subnet_name = self.read_cache("info",path=self.region)["vpc"],self.read_cache("info",path=self.region)["subnet"]
            

                errou = True
                while errou:
                    try:
                        resource_type = int(input(self.format_choice(self.resources_type)))
                        errou = False
                    except:
                        print("\n\n Algo deu errado. Tente escolher novamente\n\n")
                    time.sleep(1)
                
                if (resource_type == 1):
                    self.build_instances()

                elif (resource_type == 2):
                    self.build_security_groups()

            elif (self.state == 3) :
                self.archive_name = "main.tf"
                print("Criar usuário")
                os.chdir("users")
                self.build_users()
                os.chdir("..")


            elif (self.state == 4) :
                options_to_apply = ["Recursos","Usuários"]
                option_chosen = int(input("\nEscolha a opção para subir\n"+self.format_choice(options_to_apply)))
                if option_chosen == 1:
                    self.region = self.regions[int(input("\nEscolha a Região\n"+self.format_choice(self.regions)))-1]
                    os.chdir(self.region)
                    ops= int(input("\nEscolha a opção para destruir\n"+self.format_choice(["Instâncias","Grupos de Segurança","Tudo"])))
                    if ops == 1:
                        os.system(f'''terraform destroy -target aws_instance.{input("Nome da Instância:")}''')
                        os.chdir("..")
                    elif ops == 2:
                         os.system(f'''terraform destroy -target aws_security_group.{input("Nome do Security Group:")}''')
                         os.chdir("..")
                    elif ops == 3:
                        os.system("rm sg")
                        os.system("rm info")
                        print("\n\n Destruindo a infraestutura na cloud\n\n")
                        time.sleep(2)
                        print("\n\nIniciando o [terraform destroy]\n\n")
                        time.sleep(1)
                        os.system("terraform destroy")
                        print("\n\n[Infraestrutura destruida]\n\n")
                        self.destroy_main()
                        os.chdir("..")
                elif option_chosen == 2:
                    os.chdir("users")
                    ops= int(input("\nEscolha a opção para destruir\n"+self.format_choice(["Específico","Todos"])))
                    if ops == 1:
                        os.system(f'''terraform destroy -target aws_iam_user.{input("Nome do Usuário:")}''')
                        os.chdir("..")
                    elif ops == 2:
                        os.system("rm users")
                        print("\n\n Destruindo a infraestutura na cloud\n\n")
                        time.sleep(2)
                        print("\n\nIniciando o [terraform destroy]\n\n")
                        time.sleep(1)
                        os.system("terraform destroy")
                        print("\n\n[Infraestrutura destruida]\n\n")
                        self.destroy_main()
                        os.chdir("..")
            
            elif (self.state == 5) :
                options_to_apply = ["Recursos","Usuários"]
                option_chosen = int(input("\nEscolha a opção para subir\n"+self.format_choice(options_to_apply)))
                if option_chosen == 1:
                    self.region = self.regions[int(input("\nEscolha a Região\n"+self.format_choice(self.regions)))-1]
                    os.chdir(self.region)
                elif option_chosen == 2:
                    os.chdir("users")

                time.sleep(2)
                print("\n\nIniciando o [terraform init]\n\n")
                time.sleep(2)
                os.system("terraform init")
                time.sleep(1)
                print("\n\nInciando o [terraform apply]")
                time.sleep(2)
                os.system("terraform apply")
                time.sleep(2)
                print("\n\n[Infraestrutura subiu]\n\n")
                os.chdir("..")
            elif (self.state == 6):
                os.system("clear")
                print("\n\n\nFechando programa...")
                time.sleep(1)
                using = False
            else:
                print("\n\n...Opss\n\n")
                time.sleep(2)
                print("rotina ainda não implementada")

        




test = Cloud()
test.interface_routines()
