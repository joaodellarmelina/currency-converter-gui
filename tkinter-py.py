import requests
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk


Api_key = 'Sua chave de API'


def get_moeda_values(moeda_entrada):
    url_base = f'https://api.freecurrencyapi.com/v1/latest?apikey={Api_key}&currencies=&base_currency={moeda_entrada}'
    try:
        resp_base = requests.get(url_base)
        resp_base.raise_for_status()
        json_base = resp_base.json()
        return json_base['data']
    except requests.exceptions.RequestException as e:
        show_custom_message("Erro", f"Erro ao obter dados: {e}", "error")
        return None

def show_custom_message(title, message, type_="info"):
    popup = ctk.CTk()
    popup.title(title)
    popup.geometry("300x150")
    
    frame = ctk.CTkFrame(popup)
    frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    label = ctk.CTkLabel(frame, text=message, wraplength=250)
    label.pack(pady=10)
    
    button = ctk.CTkButton(frame, text="OK", command=popup.destroy)
    button.pack(pady=10)
    
    popup.mainloop()

def converter():
    moeda_entrada = moeda_entrada_var.get()
    moeda_sacar = moeda_saida_var.get()
    quantidade = quantidade_var.get()
    
    if not quantidade.replace('.', '', 1).isdigit():
        show_custom_message("Erro", "Por favor, insira um valor numérico válido.", "error")
        return
    
    quantidade = float(quantidade)
    
    if moeda_entrada == moeda_sacar:
        show_custom_message("Resultado", f"O valor convertido é: {quantidade:.2f} {moeda_sacar}")
        return
    
    taxas = get_moeda_values(moeda_entrada)
    if taxas and moeda_sacar in taxas:
        convertido = quantidade * taxas[moeda_sacar]
        show_custom_message("Resultado", f"O valor convertido é: {convertido:.2f} {moeda_sacar}")
    else:
        show_custom_message("Erro", "Não foi possível obter a taxa de câmbio.", "error")

moedas_disponiveis = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]

root = ctk.CTk()
root.title("Conversor de Moedas")
root.geometry("400x300")

frame = ctk.CTkFrame(root)
frame.pack(expand=True, fill='both', padx=20, pady=20)

moeda_entrada_var = tk.StringVar()
moeda_saida_var = tk.StringVar()
quantidade_var = tk.StringVar()

ctk.CTkLabel(frame, text="Moeda de Entrada:").pack(pady=5)
entrada_menu = ctk.CTkComboBox(frame, variable=moeda_entrada_var, values=moedas_disponiveis)
entrada_menu.pack(pady=5)
entrada_menu.set(moedas_disponiveis[0])

ctk.CTkLabel(frame, text="Moeda de Saída:").pack(pady=5)
saida_menu = ctk.CTkComboBox(frame, variable=moeda_saida_var, values=moedas_disponiveis)
saida_menu.pack(pady=5)
saida_menu.set(moedas_disponiveis[1])

ctk.CTkLabel(frame, text="Quantidade:").pack(pady=5)
quantidade_entry = ctk.CTkEntry(frame, textvariable=quantidade_var)
quantidade_entry.pack(pady=5)

ctk.CTkButton(frame, text="Converter", command=converter).pack(pady=10)

root.mainloop()