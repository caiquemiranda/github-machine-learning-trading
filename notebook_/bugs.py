import yfinance as yf
import pandas as pd

def download_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_standard_deviation(data, window):
    return data['Close'].rolling(window=window).std()

ticker_symbol = 'AAPL'  # Substitua 'AAPL' pelo ticker do ativo financeiro desejado
start_date = '2022-01-01'  # Defina a data de início do histórico de dados
end_date = '2023-06-01'  # Defina a data de término do histórico de dados
moving_average_window = 21  # Janela da média móvel (20 dias neste exemplo)
num_standard_deviations = 2  # Número de desvios padrão para a banda superior e inferior
stop_loss_percent = 0.05  # Valor percentual para o stop loss (5% neste exemplo)

# Baixar dados históricos do Yahoo Finance
data = download_historical_data(ticker_symbol, start_date, end_date)

def trading_strategy(data, ma_window, num_std, stop_loss_percent):
    data['SMA'] = calculate_moving_average(data, ma_window)
    data['Upper_Band'] = data['SMA'] + (data['Close'].rolling(window=ma_window).std() * num_std)
    data['Lower_Band'] = data['SMA'] - (data['Close'].rolling(window=ma_window).std() * num_std)
    data['Signal'] = 0
    data['Position'] = 0

    for i in range(ma_window, len(data)):
        if data['Close'][i] > data['Upper_Band'][i]:
            data['Signal'][i] = -1  # Sinal de venda
        elif data['Close'][i] < data['Lower_Band'][i]:
            data['Signal'][i] = 1  # Sinal de compra

        if data['Position'][i - 1] == 1 and data['Cumulative_Returns'][i] < (1 - stop_loss_percent):
            data['Signal'][i] = -1  # Aciona o stop loss e vende a posição
            data['Position'][i] = 0
        elif data['Position'][i - 1] == -1 and data['Cumulative_Returns'][i] > 0:
            data['Signal'][i] = 1  # Venda a descoberto, aciona o stop loss e compra a posição
            data['Position'][i] = 0
        else:
            data['Position'][i] = data['Signal'][i]  # Mantém a posição atual

    data.dropna(inplace=True)
    return data

# Aplicar a estratégia de trading com stop loss
data_with_signals = trading_strategy(data, moving_average_window, num_standard_deviations, stop_loss_percent)