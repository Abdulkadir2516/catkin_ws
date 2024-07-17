import cv2
import numpy as np

# RGB rengi tanımla
rgb_color = np.uint8([[[174, 101, 36]]])

# RGB'den HSV'ye dönüşüm yap
hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)
h, s, v = hsv_color[0][0]

print("HSV Değeri:", hsv_color[0][0])

# Renk aralığını belirle
lower_bound = np.array([h-10, max(s-40, 0), max(v-40, 0)], dtype=np.uint8)
upper_bound = np.array([h+10, min(s+40, 255), min(v+40, 255)], dtype=np.uint8)

print("Alt Sınır:", lower_bound)
print("Üst Sınır:", upper_bound)