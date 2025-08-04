import sounddevice as sd
import numpy as np
import pygame

# === Налаштування ===
fs = 44100  # Частота дискретизації
chunk = 1024  # Кількість семплів за кадр
width, height = 800, 400

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Live Audio (Mic)")
clock = pygame.time.Clock()

# Початкові дані
data = np.zeros(chunk)


# Функція отримання аудіо
def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)
    data = indata[:, 0] * (height // 2)  # Масштабуємо під екран


# Запуск мікрофона
stream = sd.InputStream(callback=audio_callback,
                        channels=1,
                        samplerate=fs,
                        blocksize=chunk,
                        dtype='float32')
stream.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Малюємо хвилю
    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)
        y = int(height / 2 + sample)
        points.append((x, y))

    if len(points) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)

    pygame.display.flip()
    clock.tick(60)

stream.stop()
pygame.quit()
