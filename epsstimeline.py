import requests
import matplotlib.pyplot as plt
import datetime
from PIL import Image

def get_epss_data(cve, dates):
    base_url = "https://api.first.org/data/v1/epss"
    epss_scores, percentiles = [], []
    
    for date in dates:
        response = requests.get(f"{base_url}?cve={cve}&date={date}")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                epss_scores.append(float(data["data"][0]["epss"]))
                percentiles.append(float(data["data"][0]["percentile"]))
            else:
                epss_scores.append(None)
                percentiles.append(None)
        else:
            print(f"Erro ao acessar a API para {date}: {response.status_code}")
            epss_scores.append(None)
            percentiles.append(None)
    
    return epss_scores, percentiles

def plot_graph(dates, epss_scores, percentiles, cve):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, epss_scores, marker='o', linestyle='-', color='b', label='EPSS Score')
    plt.plot(dates, percentiles, marker='s', linestyle='-', color='r', label='Percentile')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.legend()
    plt.grid()
    plt.title(f"EPSS Timeline for {cve}")
    
    # Salvar o gráfico como PNG
    png_filename = f"epss_timeline_{cve}.png"
    plt.savefig(png_filename)
    
    # Mostrar o gráfico no matplotlib (em vez de depender do Pillow)
    plt.show()
    
    plt.close()
    
    return png_filename

def open_image(png_filename):
    try:
        # Tentar abrir e exibir com PIL
        img = Image.open(png_filename)
        img.show()
    except Exception as e:
        print(f"Erro ao tentar abrir a imagem: {e}")

def main():
    cve = input("Digite o CVE (ex: CVE-2022-29056): ")
    dates_input = input("Digite 3 datas de consulta no formato YYYY-MM-DD, separadas por vírgula: ")
    dates = dates_input.split(',')
    
    if len(dates) != 3:
        print("Por favor, insira exatamente 3 datas.")
        return
    
    epss_scores, percentiles = get_epss_data(cve, dates)
    
    # Gerar gráfico e salvar em PNG
    png_filename = plot_graph(dates, epss_scores, percentiles, cve)
    
    # Tentar abrir a imagem gerada
    open_image(png_filename)

if __name__ == "__main__":
    main()
