import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QFileDialog,
    QMessageBox,
)
from moviepy.editor import VideoFileClip

class VideoToAudioConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video to Audio Converter")

        self.upload_button = QPushButton("Video Dosyası Yükle")
        self.upload_button.clicked.connect(self.upload_video)

        self.convert_button = QPushButton("Dönüştür")
        self.convert_button.clicked.connect(self.convert_video)

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_audio)
        self.save_button.setEnabled(False)

        self.file_label = QLabel("Seçilen dosya: ")
        self.output_dir_label = QLabel("Kaydedilecek klasör: ")
        self.output_dir_text = QLineEdit()
        self.browse_button = QPushButton("Gözat")
        self.browse_button.clicked.connect(self.select_output_directory)

        layout = QVBoxLayout()
        layout.addWidget(self.upload_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.output_dir_label)
        layout.addWidget(self.output_dir_text)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.selected_video = ""
        self.audio_file_path = ""
        self.output_dir = ""

    def upload_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        video_file, _ = QFileDialog.getOpenFileName(
            self, "Video Dosyası Yükle", "", "Video Files (*.mp4)", options=options
        )
        if video_file:
            self.selected_video = video_file
            self.file_label.setText("Seçilen dosya: " + video_file)
            self.save_button.setEnabled(True)

    def convert_video(self):
        if self.selected_video:
            try:
                video = VideoFileClip(self.selected_video)
                self.audio_file_path = os.path.splitext(self.selected_video)[0] + ".mp3"
                video.audio.write_audiofile(self.audio_file_path)
                print("Dönüştürme başarılı.")
                QMessageBox.information(self, "Başarılı", "Video dönüştürme işlemi başarıyla tamamlandı.")
            except Exception as e:
                print("Dönüştürme sırasında hata oluştu:", e)
                QMessageBox.critical(self, "Hata", "Video dönüştürme sırasında bir hata oluştu:\n" + str(e))
        else:
            print("Lütfen bir video dosyası seçin.")
            QMessageBox.warning(self, "Uyarı", "Lütfen bir video dosyası seçin.")

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Kaydedilecek Klasörü Seç", "", QFileDialog.ShowDirsOnly
        )
        if directory:
            self.output_dir = directory
            self.output_dir_text.setText(directory)

    def save_audio(self):
        if self.audio_file_path:
            if not self.output_dir:
                QMessageBox.warning(self, "Uyarı", "Lütfen kaydedilecek klasörü seçin.")
                return
            try:
                output_path = os.path.join(self.output_dir, os.path.basename(self.audio_file_path))
                os.rename(self.audio_file_path, output_path)
                print("Dosya başarıyla kaydedildi.")
                QMessageBox.information(self, "Başarılı", "Dosya başarıyla kaydedildi.")
            except Exception as e:
                print("Kaydetme sırasında hata oluştu:", e)
                QMessageBox.critical(self, "Hata", "Dosyayı kaydederken bir hata oluştu:\n" + str(e))
        else:
            print("Lütfen önce bir video dosyasını dönüştürün.")
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir video dosyasını dönüştürün.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoToAudioConverter()
    window.show()
    sys.exit(app.exec_())
