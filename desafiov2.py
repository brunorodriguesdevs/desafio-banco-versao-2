# Lista para armazenar os usuários
usuarios = []

# Lista para armazenar as contas correntes
contas_correntes = []

# Contador para gerar números de conta sequenciais
numero_conta_sequencial = 0

# Função para criar usuário
def criar_usuario():
    while True:
        nome = input("Informe o nome do usuário: ")
        data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
        cpf = input("Informe o CPF do usuário: ").replace(".", "").replace("-", "") 
        endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/estado): ")

        # Verifica se já existe um usuário com o mesmo CPF
        if any(user['cpf'] == cpf for user in usuarios):
            print("Já existe um usuário cadastrado com este CPF. Por favor, informe outro CPF.")
        else:
            # Adiciona o novo usuário à lista
            usuarios.append({
                'nome': nome,
                'data_nascimento': data_nascimento,
                'cpf': cpf,
                'endereco': endereco
            })
            print("Usuário cadastrado com sucesso!")
            return {'nome': nome, 'cpf': cpf}

# Função para criar conta corrente
def criar_conta_corrente():
    global numero_conta_sequencial
    usuario = criar_usuario()
    numero_conta_sequencial += 1
    return {
        'agencia': '0001',
        'numero_conta': numero_conta_sequencial,
        'usuario': usuario['nome']
    }

# Função para listar contas correntes
def listar_contas_correntes():
    print("\n=== Lista de Contas Correntes ===")
    for conta in contas_correntes:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Usuário: {conta['usuario']}")

# Função para realizar depósito
def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

# Função para realizar saque
def sacar(*, saldo, valor, extrato, limite, numero_saque, limite_saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saque >= limite_saque

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        print("Saque realizado com sucesso.")

    return saldo, extrato

# Função para exibir extrato
def exibir_extrato(*, saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else '\n'.join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Menu principal
menu = """
[c] Criar Conta Corrente
[l] Listar Contas Correntes
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

while True:
    opcao = input(menu)

    if opcao == "c":
        nova_conta = criar_conta_corrente()
        contas_correntes.append(nova_conta)
        print("Conta corrente criada com sucesso!")

    elif opcao == "l":
        listar_contas_correntes()

    elif opcao == "d":
        conta = int(input("Informe o número da conta: "))
        valor_deposito = float(input("Informe o valor do depósito: "))
        saldo_conta = contas_correntes[conta - 1]['saldo']
        extrato_conta = contas_correntes[conta - 1]['extrato']
        saldo_conta, extrato_conta = depositar(saldo_conta, valor_deposito, extrato_conta)
        contas_correntes[conta - 1]['saldo'] = saldo_conta
        contas_correntes[conta - 1]['extrato'] = extrato_conta

    elif opcao == "s":
        conta = int(input("Informe o número da conta: "))
        valor_saque = float(input("Informe o valor do saque: "))
        saldo_conta = contas_correntes[conta - 1]['saldo']
        extrato_conta = contas_correntes[conta - 1]['extrato']
        limite_conta = contas_correntes[conta - 1]['limite']
        num_saque_conta = contas_correntes[conta - 1]['numero_saque']
        limite_saque_conta = contas_correntes[conta - 1]['limite_saque']
        saldo_conta, extrato_conta = sacar(saldo=saldo_conta, valor=valor_saque, extrato=extrato_conta,
                                           limite=limite_conta, numero_saque=num_saque_conta,
                                           limite_saque=limite_saque_conta)
        contas_correntes[conta - 1]['saldo'] = saldo_conta
        contas_correntes[conta - 1]['extrato'] = extrato_conta

    elif opcao == "e":
        conta = int(input("Informe o número da conta: "))
        saldo_conta = contas_correntes[conta - 1]['saldo']
        extrato_conta = contas_correntes[conta - 1]['extrato']
        exibir_extrato(saldo=saldo_conta, extrato=extrato_conta)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
