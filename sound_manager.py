"""
Модуль для управления звуками
"""
import pygame
import config

# Попытка импорта numpy для генерации звуков
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class SoundManager:
    """Класс для управления звуковыми эффектами"""
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
        if config.SOUND_ENABLED:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._create_sounds()
    
    def _generate_tone(self, frequency: float, duration: float, volume: float = 0.3):
        """Генерация простого тонального звука"""
        if not HAS_NUMPY:
            return None
        
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)
            max_sample = 2**(16 - 1) - 1
            
            for i in range(frames):
                wave = max_sample * volume * np.sin(2 * np.pi * frequency * i / sample_rate)
                arr[i][0] = int(wave)  # Левый канал
                arr[i][1] = int(wave)  # Правый канал
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except Exception:
            return None
    
    def _create_sounds(self):
        """Создание звуковых эффектов программно"""
        if not HAS_NUMPY:
            print("Numpy не установлен. Звуки отключены. Установите: pip install numpy")
            return
        
        try:
            # Звук поимки шара - приятный высокий тон
            catch_sound = self._generate_tone(800, 0.15, 0.2)
            if catch_sound:
                self.sounds['catch'] = catch_sound
            
            # Звук промаха - низкий грустный тон
            miss_sound = self._generate_tone(300, 0.3, 0.25)
            if miss_sound:
                self.sounds['miss'] = miss_sound
            
            # Звук отскока от полочки - короткий средний тон
            bounce_sound = self._generate_tone(600, 0.1, 0.15)
            if bounce_sound:
                self.sounds['bounce'] = bounce_sound
            
            # Звук повышения сложности - восходящий тон
            levelup_sound = self._generate_tone(1000, 0.4, 0.3)
            if levelup_sound:
                self.sounds['levelup'] = levelup_sound
        except Exception as e:
            print(f"Ошибка создания звуков: {e}")
    
    def play_sound(self, sound_name: str):
        """Воспроизведение звука"""
        if config.SOUND_ENABLED and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                pass  # Тихая ошибка, чтобы не мешать игре
    
    def play_music(self, loop: bool = True):
        """Воспроизведение музыки"""
        # Музыка отключена по умолчанию, так как требует файл
        pass
    
    def stop_music(self):
        """Остановка музыки"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

