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

- Esta aplicação permite que você consiga construir infrastrutura nas regiões: 
 * `us-east-1` (North Virginia)
 * `us-east-2` (Ohio)
 
 Para que isso aconteça, é necessário que você configure na sua conta AWS a permissão de Administrador, desse modo você pode ter acesso a mais de uma região. Nesse sentido, caso sua conta não possua a permissão, é necessário você atualizar, afim de que essa aplicação possa ser utilizada.
 
> **Note**

> O HA de Web Servers está construindo somente para a região `us-east-2`.

### Criar uma KEY PAIR

- Esta aplicação, possui HA de servidores na região `us-east-2`, por essa razão é necessário que você crie uma *KEY PAIR* no dashboard da AWS para tal região.
 
 
 ## Utilizando Essa Aplicação
 
 * Antes de tudo, será necessário você clonar esse repositório:
 > `https://github.com/jeansilas/Cloud-Project-AWS-Terraform`
 
 
 Com o Repositório na sua máquina local, será necessário você acessar o arquivo: `"Cloud-Project-AWS-Terraform/us-east-2/autoscaling.tf"`
 
 Na linha 92, haverá um campo nomeado `"key_name"`. Basta você trocar o nome que está ali (JanPair), pelo nome que você deu para KEY PAIR criada.
 
 Ex:
 
```[88] resource "aws_launch_configuration" "scaling" {

[89]  name_prefix     = "learn-terraform-aws-asg-"
[90]  image_id        = "ami-0a59f0e26c55590e9"
[91]  instance_type   = "t2.micro"
[92]  key_name = "JanPair"
[93]  security_groups = [aws_security_group.instance-sg.id]
[94]
[95]  lifecycle {
[96]    create_before_destroy = true
[97]  }
[98]}
```

Uma vez na pasta raiz da aplicação, para começar a aplicação, basta digitar no terminal: `python3 app.py` ou `python app.py`



E a aplicação estará pronta para ser utilizada.

> **Warning**

![oie_7ABqu3U6i2mm](https://user-images.githubusercontent.com/39682690/204158848-24f579d1-3acf-4b1e-ba73-6038a0c81113.png)

Importante ter preocaução de *NA GRANDE MAIORIA DAS VEZES* quando for criar recursos, sempre optar por não resscrever o main.tf, ou seja sempre optar por 0. No caso da região `us-east-2`, não recomendo de *JEITO NENHUM* destruir ou rescrever, para não mexer com o webserver na AWS.
> **Warning**

## Considerações Finais:

Essa aplicação ainda possui bastante passos para melhoramento, então caso tenha algum feedback, mande um pull request para esse repositório. De resto, espero que essa aplicação possa ser útil de alguma forma para você.

## Referências:
- [AWS](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Tutorial Inicial de Utilização do Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)
- [Tutorial para HA no Terraform](https://developer.hashicorp.com/terraform/tutorials/aws/aws-asg)
