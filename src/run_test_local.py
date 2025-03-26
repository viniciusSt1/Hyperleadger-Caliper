import os
import subprocess
from datetime import datetime

# Caminhos para cada configuração de função
BENCHMARK_FILES = {
    "getLatestStatus": 'benchmarks/scenario-monitoring/NodeHealthMonitor/config-getLatestStatus.yaml',
    "reportStatus": 'benchmarks/scenario-monitoring/NodeHealthMonitor/config-reportStatus.yaml',
    "statusReports": 'benchmarks/scenario-monitoring/NodeHealthMonitor/config-statusReports.yaml'
}

# TPS a ser testado (20 a 120, de 20 em 20)
#TPS_LIST = [20, 40, 60, 80, 100, 120]
TPS_LIST = [140, 160, 180, 200]

# Atualiza o valor de TPS no arquivo de benchmark YAML
def update_tps_in_file(file_path, tps):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("tps:"):
            new_lines.append(f"          tps: {tps}\n")
        else:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Executa o Caliper para uma função e TPS
def run_test(tps, function_name, benchmark_file):
    update_tps_in_file(benchmark_file, tps)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_dir = f"reports/{function_name}"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{function_name}_report_{tps}_{timestamp}.html")

    cmd = [
        'npx', 'caliper', 'launch', 'manager',
        '--caliper-workspace', './',
        '--caliper-benchconfig', benchmark_file,
        '--caliper-networkconfig', 'networks/besu/networkconfig.json',
        '--caliper-bind-sut', 'besu:latest',
        '--caliper-flow-skip-install'
    ]

    subprocess.run(cmd)

    if os.path.exists('report.html'):
        os.rename('report.html', report_path)
        print(f"✅ Relatório salvo em {report_path}")
    else:
        print(f"⚠️ Relatório não encontrado para {function_name} @ {tps} TPS.")

# Executa todos os testes
if __name__ == "__main__":
    for function_name, benchmark_file in BENCHMARK_FILES.items():
        print(f"\n🚀 Iniciando testes para função: {function_name}")
        for tps in TPS_LIST:
            run_test(tps, function_name, benchmark_file)
