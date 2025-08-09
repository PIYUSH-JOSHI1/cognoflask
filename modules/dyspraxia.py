from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from utils.file_manager import file_manager
import cv2
import numpy as np
import base64
import io
from PIL import Image
import json

dyspraxia_bp = Blueprint('dyspraxia', __name__)

class DyspraxiaAI:
    def __init__(self):
        self.balance_exercises = [
            {
                'name': 'Single Leg Stand',
                'description': 'Stand on one foot for the target duration',
                'instructions': 'Lift one foot off the ground and maintain balance. Use your arms for stability.',
                'duration': 10,
                'difficulty': 'easy',
                'tips': ['Focus on a fixed point ahead', 'Keep your core engaged', 'Breathe normally']
            },
            {
                'name': 'Heel-to-Toe Walk',
                'description': 'Walk in a straight line placing heel directly in front of toe',
                'instructions': 'Walk forward in a straight line, placing your heel directly in front of your toe with each step.',
                'duration': 15,
                'difficulty': 'medium',
                'tips': ['Look ahead, not down', 'Take your time', 'Keep arms out for balance']
            },
            {
                'name': 'Balance Beam Walk',
                'description': 'Walk along an imaginary line maintaining balance',
                'instructions': 'Imagine a straight line on the floor and walk along it without stepping off.',
                'duration': 20,
                'difficulty': 'medium',
                'tips': ['Start slowly', 'Use peripheral vision', 'Practice daily for improvement']
            },
            {
                'name': 'Eyes Closed Balance',
                'description': 'Balance on one foot with eyes closed',
                'instructions': 'Close your eyes and balance on one foot. This challenges your proprioception.',
                'duration': 8,
                'difficulty': 'hard',
                'tips': ['Start with eyes open', 'Have someone nearby for safety', 'Focus on body awareness']
            },
            {
                'name': 'Dynamic Balance',
                'description': 'Balance while moving your arms',
                'instructions': 'Stand on one foot while moving your arms in different directions.',
                'duration': 12,
                'difficulty': 'hard',
                'tips': ['Start with small movements', 'Gradually increase range', 'Maintain core stability']
            }
        ]
        
        self.coordination_games = [
            {
                'name': 'Rock Paper Scissors',
                'description': 'Play against computer using hand gestures',
                'instructions': 'Make rock, paper, or scissors gestures with your hand',
                'type': 'gesture_recognition',
                'rounds': 5
            },
            {
                'name': 'Simon Says Gestures',
                'description': 'Follow gesture commands in sequence',
                'instructions': 'Copy the gestures shown on screen in the correct order',
                'type': 'sequence_memory',
                'rounds': 5
            },
            {
                'name': 'Target Pointing',
                'description': 'Point at targets that appear on screen',
                'instructions': 'Point your finger at the red targets as they appear',
                'type': 'precision_pointing',
                'rounds': 10
            }
        ]
    
    def analyze_pose_stability(self, pose_landmarks):
        """Analyze pose stability from MediaPipe landmarks"""
        if not pose_landmarks:
            return {'stability': 0, 'feedback': 'No pose detected', 'suggestions': []}
        
        # Calculate center of mass
        # This is a simplified version - in production use proper biomechanical calculations
        hip_left = pose_landmarks.get('left_hip', {})
        hip_right = pose_landmarks.get('right_hip', {})
        
        if not hip_left or not hip_right:
            return {'stability': 50, 'feedback': 'Partial pose detected', 'suggestions': ['Stand fully in view of camera']}
        
        # Calculate stability metrics
        center_x = (hip_left.get('x', 0) + hip_right.get('x', 0)) / 2
        center_y = (hip_left.get('y', 0) + hip_right.get('y', 0)) / 2
        
        # Simulate stability calculation (in production, track movement over time)
        stability_score = min(100, max(0, 100 - abs(center_x - 0.5) * 200))
        
        feedback = []
        suggestions = []
        
        if stability_score > 80:
            feedback.append("Excellent balance!")
            suggestions.append("Try closing your eyes for added challenge")
        elif stability_score > 60:
            feedback.append("Good balance, keep practicing")
            suggestions.append("Focus on a fixed point ahead")
        else:
            feedback.append("Keep working on your balance")
            suggestions.append("Use your arms for stability")
            suggestions.append("Practice daily for improvement")
        
        return {
            'stability': stability_score,
            'feedback': feedback,
            'suggestions': suggestions,
            'center_of_mass': {'x': center_x, 'y': center_y}
        }
    
    def detect_hand_gesture(self, hand_landmarks):
        """Detect hand gestures from MediaPipe landmarks"""
        if not hand_landmarks:
            return 'none'
        
        # Simplified gesture detection
        # In production, implement proper gesture recognition using hand landmark positions
        
        # For demo purposes, simulate gesture detection
        gestures = ['rock', 'paper', 'scissors', 'point', 'thumbs_up', 'wave']
        import random
        return random.choice(gestures)
    
    def generate_balance_exercise(self, difficulty='easy'):
        """Generate a balance exercise based on difficulty"""
        exercises = [ex for ex in self.balance_exercises if ex['difficulty'] == difficulty]
        if not exercises:
            exercises = self.balance_exercises
        
        import random
        return random.choice(exercises)
    
    def evaluate_balance_performance(self, duration, stability_scores):
        """Evaluate balance performance based on duration and stability"""
        if not stability_scores:
            return {'score': 0, 'feedback': 'No data recorded', 'improvement_tips': []}
        
        avg_stability = sum(stability_scores) / len(stability_scores)
        completion_rate = min(100, (duration / 10) * 100)  # Assuming 10s target
        
        overall_score = (avg_stability * 0.7) + (completion_rate * 0.3)
        
        feedback = []
        tips = []
        
        if overall_score >= 85:
            feedback.append("Outstanding performance!")
            tips.append("Try more challenging exercises")
        elif overall_score >= 70:
            feedback.append("Great improvement!")
            tips.append("Focus on holding positions longer")
        elif overall_score >= 50:
            feedback.append("Good effort, keep practicing")
            tips.append("Practice daily for better results")
            tips.append("Focus on core strength")
        else:
            feedback.append("Keep working at it!")
            tips.append("Start with easier exercises")
            tips.append("Consider working with a therapist")
        
        return {
            'score': round(overall_score, 1),
            'avg_stability': round(avg_stability, 1),
            'completion_rate': round(completion_rate, 1),
            'feedback': feedback,
            'improvement_tips': tips
        }

dyspraxia_ai = DyspraxiaAI()

@dyspraxia_bp.route('/')
def main():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dyspraxia/main.html')

@dyspraxia_bp.route('/balance-training')
def balance_training():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dyspraxia/balance_training.html')

@dyspraxia_bp.route('/get-balance-exercise', methods=['POST'])
def get_balance_exercise():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    difficulty = data.get('difficulty', 'easy')
    
    try:
        exercise = dyspraxia_ai.generate_balance_exercise(difficulty)
        
        return jsonify({
            'success': True,
            'exercise': exercise
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating exercise: {str(e)}'
        }), 500

@dyspraxia_bp.route('/coordination-games')
def coordination_games():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dyspraxia/coordination_games.html')

@dyspraxia_bp.route('/submit-balance-result', methods=['POST'])
def submit_balance_result():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    exercise_name = data.get('exercise_name', '')
    duration = data.get('duration', 0)
    stability = data.get('stability', 0)
    
    try:
        # Save progress
        progress_data = {
            'user_id': session['user_id'],
            'activity': 'balance_training',
            'exercise_name': exercise_name,
            'duration': duration,
            'stability_score': stability,
            'timestamp': file_manager.get_timestamp()
        }
        
        fieldnames = ['user_id', 'activity', 'exercise_name', 'duration', 'stability_score', 'timestamp']
        file_manager.append_csv('data/dyspraxia/progress.csv', progress_data, fieldnames)
        
        return jsonify({
            'success': True,
            'message': 'Progress saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving progress: {str(e)}'
        }), 500

@dyspraxia_bp.route('/camera-exercises')
def camera_exercises():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dyspraxia/camera_exercises.html')

@dyspraxia_bp.route('/analyze-pose', methods=['POST'])
def analyze_pose():
    """Analyze pose data from camera feed"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    pose_data = data.get('pose_landmarks', {})
    
    try:
        analysis = dyspraxia_ai.analyze_pose_stability(pose_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error analyzing pose: {str(e)}'
        }), 500

@dyspraxia_bp.route('/detect-gesture', methods=['POST'])
def detect_gesture():
    """Detect hand gestures from camera feed"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    hand_landmarks = data.get('hand_landmarks', {})
    
    try:
        gesture = dyspraxia_ai.detect_hand_gesture(hand_landmarks)
        
        return jsonify({
            'success': True,
            'gesture': gesture
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error detecting gesture: {str(e)}'
        }), 500
