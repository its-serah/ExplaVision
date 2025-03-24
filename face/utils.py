import cv2
import numpy as np
import dlib
import asyncio
from telegram import Bot
from django.conf import settings
from typing import Union, Optional
from pathlib import Path


def align_face(face_img):
    """
    Align a detected face image by rotating it to make the eyes horizontal.

    This function uses dlib's facial landmark detector to identify the positions of the eyes,
    then rotates the image to align the eyes horizontally, which improves face recognition accuracy.

    Args:
        face_img (numpy.ndarray): The input face image as a NumPy array (BGR format from OpenCV)

    Returns:
        numpy.ndarray: The aligned face image, or the original image if no face is detected
    """
    # Initialize dlib's face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        "shape_predictor_68_face_landmarks.dat"
    )  # Pre-trained model file required

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = detector(gray)

    # If no faces are detected, return the original image
    if len(faces) == 0:
        return face_img  # No alignment needed

    # Process the first detected face
    for face in faces:
        # Get 68 facial landmarks for the face
        landmarks = predictor(gray, face)

        # Extract eye coordinates (points 36 and 45 are the outer corners of left and right eyes)
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)

        # Calculate angle needed to align eyes horizontally
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dy, dx))

        # Perform image rotation to align eyes horizontally
        center = (face_img.shape[1] // 2, face_img.shape[0] // 2)  # Center of the image
        M = cv2.getRotationMatrix2D(center, angle, 1)  # Rotation matrix
        aligned = cv2.warpAffine(face_img, M, (face_img.shape[1], face_img.shape[0]))

        return aligned


async def send_telegram_message(
    message: str, image_path: Optional[Union[str, Path]] = None
) -> bool:
    """
    Send a message and optionally an image to the configured Telegram channel asynchronously.

    This function handles sending notifications to a Telegram channel when faces are recognized
    or when errors occur. It can send both text messages and images.

    Args:
        message (str): The text message to send to the Telegram channel
        image_path (Optional[Union[str, Path]]): Optional path to an image file to send

    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        print("Sending Telegram message...")  # Debugging output
        # Check if Telegram bot is configured
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHANNEL_ID:
            return False  # Cannot send message if bot or channel not configured
        
        # Initialize the Telegram bot
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        # Send message with photo if image_path is provided
        if image_path:
            with open(image_path, "rb") as photo:
                await bot.send_photo(
                    chat_id=settings.TELEGRAM_CHANNEL_ID, photo=photo, caption=message
                )
        else:
            # Send text-only message
            await bot.send_message(chat_id=settings.TELEGRAM_CHANNEL_ID, text=message)

        return True  # Message sent successfully
    except Exception as e:
        # Log error but don't crash the application
        print(f"Error sending Telegram message: {e}")
        return False


def send_telegram_message_sync(
    message: str, image_path: Optional[Union[str, Path]] = None
) -> bool:
    """
    Synchronous wrapper for the asynchronous send_telegram_message function.

    This function allows sending Telegram messages from synchronous code by
    creating a new event loop to run the asynchronous function.

    Args:
        message (str): The text message to send to the Telegram channel
        image_path (Optional[Union[str, Path]]): Optional path to an image file to send

    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    return asyncio.run(send_telegram_message(message, image_path))
