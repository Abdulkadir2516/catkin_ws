import pandas as pd

# Örnek veriyi bir CSV dosyasından okuyalım
df = pd.read_csv('~/drone_positions.csv')

# Yeni sütunlar oluşturmak için listeler
average_y = []
x_values = []

# Başlangıç değerleri
previous_y = df['y'].iloc[0]
previous_x = df['x'].iloc[0]
temp_values_y = [previous_y]
temp_values_x = [previous_x]

# y değerlerinin arasındaki farkı kontrol ederek ortalama hesaplayalım ve x değerlerini ekleyelim
for x, y in zip(df['x'].iloc[1:], df['y'].iloc[1:]):
    if abs(y - previous_y) < 1.2:
        temp_values_y.append(y)
        temp_values_x.append(x)
    else:
        if temp_values_y:
            average_y.append(sum(temp_values_y) / len(temp_values_y))
            x_values.append(temp_values_x[0])  # İlk x değerini ekle
            temp_values_y = [y]
            temp_values_x = [x]
        else:
            average_y.append(y)
            x_values.append(x)
    previous_y = y

# Son grubu da ekleyelim
if temp_values_y:
    average_y.append(sum(temp_values_y) / len(temp_values_y))
    x_values.append(temp_values_x[0])

# Ortalamaları ve x değerlerini yeni sütunlar olarak ekleyelim
df['x_values'] = pd.Series(x_values)
df['average_y'] = pd.Series(average_y)

# Sonucu yeni bir CSV dosyasına kaydedelim
df.to_csv('./processed_data.csv', index=False)

#import ace_tools as tools; tools.display_dataframe_to_user(name="Processed Data", dataframe=df)
