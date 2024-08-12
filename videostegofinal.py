from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import os
print(cv2.__version__)
print(np.__version__)

class VideoSteganography:
    def __init__(self):
        self.video_file_path = ""
        self.output_file_path = ""
    
    def main(self, root):
        root.title('Video Steganography')
        root.geometry('500x600')
        root.resizable(width=True, height=True)
        root.config(bg='#e3f4f1')
        frame = Frame(root)
        frame.grid()

        title = Label(frame, text='Video Steganography')
        title.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        title.grid(pady=10)
        title.grid(row=1)

        encode = Button(frame, text="Encode", command=lambda: self.encode_frame1(frame), padx=14, bg='#e3f4f1')
        encode.config(font=('Courier', 14), bg='#e8c1c7')
        encode.grid(row=2)

        decode = Button(frame, text="Decode", command=lambda: self.decode_frame1(frame), padx=14, bg='#e3f4f1')
        decode.config(font=('Courier', 14), bg='#e8c1c7')
        decode.grid(pady=12, row=3)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def back(self, frame):
        frame.destroy()
        self.main(root)

    def encode_frame1(self, F):
        F.destroy()
        F2 = Frame(root)

        label1 = Label(F2, text='Select the Video File in which \nyou want to hide text:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        button_bws = Button(F2, text='Select', command=lambda: self.encode_frame2(F2))
        button_bws.config(font=('Courier', 18), bg='#e8c1c7')
        button_bws.grid()

        button_back = Button(F2, text='Cancel', command=lambda: self.back(F2))
        button_back.config(font=('Courier', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()

    def encode_frame2(self, e_F2):
        e_pg = Frame(root)
        self.video_file_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4;*.avi;*.mkv;*.flv;*.mov'),
                                                                     ('All Files', '*.*')])

        if not self.video_file_path:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            label3 = Label(e_pg, text='Selected Video File')
            label3.config(font=('', 14, 'bold'))
            label3.grid()

            label_file = Label(e_pg, text=self.video_file_path)
            label_file.config(font=('', 12))
            label_file.grid()

            label2 = Label(e_pg, text='Enter the message:')
            label2.config(font=('Courier', 14, 'bold'))
            label2.grid(pady=15)

            text_a = Text(e_pg, width=50, height=10)
            text_a.grid()

            encode_button = Button(e_pg, text='Encode', command=lambda: [self.encode_video(text_a), self.back(e_pg)])
            encode_button.config(font=('Courier', 14), bg='#e8c1c7')
            encode_button.grid(pady=15)

            e_pg.grid(row=1)
            e_F2.destroy()

    def encode_video(self, text_a):
        data = text_a.get("1.0", "end-1c")

        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
            return

        try:
            cap = cv2.VideoCapture(self.video_file_path)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_path = os.path.splitext(self.video_file_path)[0] + "_with_text.avi"
            out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Embed the message in the first frame
                frame = self.embed_text_in_frame(frame, data)
                
                out.write(frame)

            cap.release()
            out.release()
            messagebox.showinfo("Success", f"Encoding Successful!\nFile is saved as {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error encoding video: {e}")

    def embed_text_in_frame(self, frame, text):
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        text_len = len(binary_text)
        frame_flat = frame.flatten()
        
        if text_len > len(frame_flat):
            raise ValueError("Text too long to encode in the video frame.")
        
        for i in range(text_len):
            frame_flat[i] = (frame_flat[i] & ~1) | int(binary_text[i])
        
        return frame_flat.reshape(frame.shape)

    def decode_frame1(self, F):
        F.destroy()
        F2 = Frame(root)

        label1 = Label(F2, text='Select the Video File from which \nyou want to extract text:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        button_bws = Button(F2, text='Select', command=lambda: self.decode_video(F2))
        button_bws.config(font=('Courier', 18), bg='#e8c1c7')
        button_bws.grid()

        button_back = Button(F2, text='Cancel', command=lambda: self.back(F2))
        button_back.config(font=('Courier', 18), bg='#e8c1c7')
        button_back.grid(pady=15)

        F2.grid()
        
    def decode_video(self, F):
        video_file = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4;*.avi;*.mkv;*.flv;*.mov'),
                                                           ('All Files', '*.*')])

        if not video_file:
            messagebox.showerror("Error", "You have selected nothing!")
            return
        
        try:
            cap = cv2.VideoCapture(video_file)
            ret, frame = cap.read()
            
            if not ret:
                raise ValueError("Could not read the video file.")
            
            message = self.extract_text_from_frame(frame)
            messagebox.showinfo("Decoded Message", message.strip())

            cap.release()

        except Exception as e:
            messagebox.showerror("Error", f"Error decoding video: {e}")

        F.destroy()

    def extract_text_from_frame(self, frame):
        binary_text = ''
        frame_flat = frame.flatten()
        
        for i in range(len(frame_flat)):
            binary_text += str(frame_flat[i] & 1)
        
        chars = [chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)]
        message = ''.join(chars)
        
        return message

# GUI loop
root = Tk()
o = VideoSteganography()
o.main(root)
root.mainloop()
