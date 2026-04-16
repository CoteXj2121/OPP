from abc import ABC, abstractmethod


class AudioPlayable(ABC):
    @abstractmethod
    def play_audio(self, file: str) -> None:
        pass


class VideoPlayable(ABC):
    @abstractmethod
    def play_video(self, file: str) -> None:
        pass


class SubtitleSupport(ABC):
    @abstractmethod
    def show_subtitles(self, file: str) -> None:
        pass


class VideoPlayer(AudioPlayable, VideoPlayable, SubtitleSupport):
    def play_audio(self, file: str) -> None:
        print(f"Воспроизведение аудио: {file}")

    def play_video(self, file: str) -> None:
        print(f"Воспроизведение видео: {file}")

    def show_subtitles(self, file: str) -> None:
        print(f"Субтитры: {file}")


class AudioPlayer(AudioPlayable):
    def play_audio(self, file: str) -> None:
        print(f"Воспроизведение аудио: {file}")


if __name__ == "__main__":
    audio_player = AudioPlayer()
    audio_player.play_audio("song.mp3")

    video_player = VideoPlayer()
    video_player.play_video("movie.mp4")
    video_player.show_subtitles("movie.srt")
