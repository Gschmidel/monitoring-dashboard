# Importa bibliotecas
import pandas as pd
import random
from faker import Faker
from datetime import timedelta

# Inicializa o Faker
fake = Faker()

# Possíveis módulos do sistema
modules = ["API", "Database", "Frontend", "Auth", "Payments"]

# Tipos de erro
error_types = ["Timeout", "Connection Error", "Auth Failure", "Data Error"]

# Níveis de severidade
severity_levels = ["Low", "Medium", "High", "Critical"]

# Status dos erros
status_list = ["Open", "In Progress", "Resolved"]

# Função principal para gerar dados
def generate_data(n=500):
    data = []

    for _ in range(n):

        # Data de criação do erro
        created_at = fake.date_time_between(start_date='-30d', end_date='now')

        # Define se o erro foi resolvido ou não
        resolved = random.choice([True, False])

        # Se foi resolvido, gera tempo de resolução
        resolved_at = created_at + timedelta(hours=random.randint(1, 72)) if resolved else None

        data.append({
            "id": fake.uuid4(),  # ID único do erro

            # Módulo onde ocorreu o erro
            "module": random.choice(modules),

            # Tipo de erro
            "error_type": random.choice(error_types),

            # Severidade do erro
            "severity": random.choice(severity_levels),

            # Status do erro
            "status": "Resolved" if resolved else random.choice(["Open", "In Progress"]),

            # Data de criação
            "created_at": created_at,

            # Data de resolução (se houver)
            "resolved_at": resolved_at
        })

    # Converte para DataFrame
    df = pd.DataFrame(data)

    # Salva no CSV
    df.to_csv("data/system_errors.csv", index=False)

    print("Dataset de erros gerado com sucesso!")

# Executa automaticamente
if __name__ == "__main__":
    generate_data() 