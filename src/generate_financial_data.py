# Importa bibliotecas necessárias
import pandas as pd              # Manipulação de dados
import random                    # Geração de valores aleatórios
from faker import Faker          # Geração de dados fictícios realistas

# Inicializa o Faker
fake = Faker()

# Listas com possíveis valores para simular dados reais
transaction_types = ["Purchase", "Refund", "Subscription"]
categories = ["E-commerce", "Fintech", "SaaS"]
status_list = ["Approved", "Failed", "Pending"]
risk_levels = ["Low", "Medium", "High"]

# Função principal para gerar dados
def generate_data(n=500):
    data = []  # Lista onde vamos armazenar os registros

    # Loop para criar n registros
    for _ in range(n):

        # Gera uma data aleatória nos últimos 30 dias
        created_at = fake.date_time_between(start_date='-30d', end_date='now')

        # Cria um registro simulando uma transação financeira
        data.append({
            "id": fake.uuid4(),  # ID único da transação

            # Tipo da transação (compra, reembolso, assinatura)
            "transaction_type": random.choice(transaction_types),

            # Categoria do negócio
            "category": random.choice(categories),

            # Valor da transação (entre 10 e 5000)
            "amount": round(random.uniform(10, 5000), 2),

            # Status da transação
            "status": random.choice(status_list),

            # Nível de risco (importante para análise de fraude/anomalia)
            "risk_level": random.choice(risk_levels),

            # Data de criação da transação
            "created_at": created_at
        })

    # Converte a lista em DataFrame
    df = pd.DataFrame(data)

    # Salva os dados em CSV
    df.to_csv("data/financial_transactions.csv", index=False)

    print("Dataset financeiro gerado com sucesso!")

# Executa a função quando o arquivo for rodado diretamente
if __name__ == "__main__":
    generate_data()