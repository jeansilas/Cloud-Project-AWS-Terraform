# Cloud-Project-AWS-Terraform 

> Autor | Jean Sanandrez



## Objetivo do Projeto:

Esse é um projeto que visa fazer a construção de uma infraestrutura na AWS de uma forma amigável, fazendo uso de ferramentas como Python e Terraform.
## Descrição:
> O que essa aplicação permite fazer:

- Implementar criação automática de VPC e sub-rede
- Listar instâncias e regiões, usuários e security_groups com regras
- Parar e iniciar instâncias
- Criação de instâncias e pelo menos 2 tipos de hosts
- Criação de security groups padrões e associação a instâncias
- Criação de usuário no IAM
- Deletar usuários, instâncias e security groups
- Regras personalizadas em security groups
- Instâncias em mais de uma região (us-east-1 e us-east-2)
- Associar restrições a usuários (apenas consultar, apenas consultar e criar e apenas consultar, criar e deletar)
- Deletar regras em security groups
- Criar um HA de servidores web 



## Terraform 

 > O Que é:
 
* O Terraform é poderoso (se não o mais poderoso que existe atualmente) e uma das ferramentas mais utilizadas que permitem o gerenciamento de infraestrutura como código (IaC). Ele permite que os desenvolvedores realizem uma grande variedade de coisas e não os restringe de fazê-las de forma com que sejam difíceis de integrar ou suportar à longo prazo.

> Como é Utilizado no Projeto:

* O python funciona como uma camada de abstração para deixar mais amigável a construção da infraestrutura, asbtraindo a sintaxe do Terraform por uma interface no terminal mais humana. Assim, o Terraform é o elemento principal da aplicação, ele que fica responsável por construir toda a infrasetrutura na AWS.

> Como Configurá-lo na sua máquina para utilizar esta aplicação:

* Primeiro Passo é instalar o Terraform:

##### Instalação do Terraform

* Basta seguir o Tutorial neste Link: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli.

Além do Terraform será necessário instalar o boto3 e a CLI da AWS.


### Instalação do CLI da AWS e do boto3 

> Instalando o Boto3:
* Basta rodar no terminal: `pip install boto3` ou `pip3 install boto3`.

> Instalando o CLI da AWS:
* Basta seguir este tutorial: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

## AWS


### Configurando as Credenciais da AWS

* De modo que você consiga logar, basta digitar `aws configure` no terminal e colocar as keys da AWS que você recebeu. (o AWS CLI precisa estar instalado)

### Atualizar a Permissão de Regiões

* Esta aplicação permite que você consiga


