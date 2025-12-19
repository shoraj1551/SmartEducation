"""
Proof of Learning Service for Feature 10: Proof-of-Learning System
Handles quiz generation, verification, and certification
"""
from datetime import datetime
from models import LearningItem, User
from mongoengine import Document, ReferenceField, StringField, IntField, BooleanField, DateTimeField, ListField, DictField
from mongoengine.errors import DoesNotExist


# New Models for Feature 10
class Quiz(Document):
    """Quiz for learning verification"""
    meta = {'collection': 'quizzes'}
    
    learning_item_id = ReferenceField(LearningItem, required=True)
    title = StringField(required=True)
    questions = ListField(DictField())  # List of question objects
    passing_score = IntField(default=70)  # Percentage required to pass
    max_attempts = IntField(default=3)
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'learning_item_id': str(self.learning_item_id.id),
            'title': self.title,
            'questions': self.questions,
            'passing_score': self.passing_score,
            'max_attempts': self.max_attempts,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class QuizAttempt(Document):
    """Quiz attempt record"""
    meta = {'collection': 'quiz_attempts'}
    
    quiz_id = ReferenceField(Quiz, required=True)
    user_id = ReferenceField(User, required=True)
    score = IntField(required=True)
    passed = BooleanField(default=False)
    answers = DictField()  # User's answers
    attempted_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'quiz_id': str(self.quiz_id.id),
            'user_id': str(self.user_id.id),
            'score': self.score,
            'passed': self.passed,
            'attempted_at': self.attempted_at.isoformat() if self.attempted_at else None
        }


class Certificate(Document):
    """Learning completion certificate"""
    meta = {'collection': 'certificates'}
    
    user_id = ReferenceField(User, required=True)
    learning_item_id = ReferenceField(LearningItem, required=True)
    certificate_type = StringField(max_length=50, default='completion')  # completion, mastery
    issued_at = DateTimeField(default=datetime.utcnow)
    verification_code = StringField(unique=True)
    is_public = BooleanField(default=False)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id.id),
            'learning_item_id': str(self.learning_item_id.id),
            'certificate_type': self.certificate_type,
            'issued_at': self.issued_at.isoformat() if self.issued_at else None,
            'verification_code': self.verification_code,
            'is_public': self.is_public
        }


class ProofOfLearningService:
    """Service for proof-of-learning system"""
    
    @staticmethod
    def create_quiz(learning_item_id, quiz_data):
        """
        Create a quiz for a learning item
        
        Args:
            learning_item_id: Learning item ID
            quiz_data: Dictionary with quiz details
            
        Returns:
            Quiz object
        """
        try:
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("Learning item not found")
        
        quiz = Quiz(
            learning_item_id=item,
            title=quiz_data.get('title', f"Quiz: {item.title}"),
            questions=quiz_data.get('questions', []),
            passing_score=quiz_data.get('passing_score', 70),
            max_attempts=quiz_data.get('max_attempts', 3)
        )
        quiz.save()
        
        return quiz
    
    @staticmethod
    def submit_quiz_attempt(quiz_id, user_id, answers):
        """
        Submit a quiz attempt
        
        Args:
            quiz_id: Quiz ID
            user_id: User ID
            answers: Dictionary of answers
            
        Returns:
            QuizAttempt object with results
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("Quiz or user not found")
        
        # Check attempt limit
        previous_attempts = QuizAttempt.objects(quiz_id=quiz, user_id=user).count()
        if previous_attempts >= quiz.max_attempts:
            raise ValueError(f"Maximum attempts ({quiz.max_attempts}) reached")
        
        # Calculate score
        score = ProofOfLearningService._calculate_quiz_score(quiz, answers)
        passed = score >= quiz.passing_score
        
        # Create attempt record
        attempt = QuizAttempt(
            quiz_id=quiz,
            user_id=user,
            score=score,
            passed=passed,
            answers=answers
        )
        attempt.save()
        
        # If passed, update learning item progress to 100%
        if passed:
            item = quiz.learning_item_id
            item.progress_percentage = 100
            item.status = 'completed'
            item.save()
        
        return attempt
    
    @staticmethod
    def _calculate_quiz_score(quiz, answers):
        """Calculate quiz score based on correct answers"""
        if not quiz.questions:
            return 0
        
        correct_count = 0
        for question in quiz.questions:
            question_id = question.get('id')
            correct_answer = question.get('correct_answer')
            user_answer = answers.get(question_id)
            
            if user_answer == correct_answer:
                correct_count += 1
        
        score = (correct_count / len(quiz.questions)) * 100
        return round(score, 2)
    
    @staticmethod
    def issue_certificate(user_id, learning_item_id, certificate_type='completion'):
        """
        Issue a certificate for completing a learning item
        
        Args:
            user_id: User ID
            learning_item_id: Learning item ID
            certificate_type: Type of certificate
            
        Returns:
            Certificate object
        """
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
            item = LearningItem.objects.get(id=learning_item_id)
        except DoesNotExist:
            raise ValueError("User or learning item not found")
        
        # Check if certificate already exists
        existing = Certificate.objects(user_id=user, learning_item_id=item).first()
        if existing:
            return existing
        
        # Generate verification code
        import hashlib
        verification_code = hashlib.sha256(
            f"{user.id}{item.id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12].upper()
        
        # Create certificate
        certificate = Certificate(
            user_id=user,
            learning_item_id=item,
            certificate_type=certificate_type,
            verification_code=verification_code
        )
        certificate.save()
        
        return certificate
    
    @staticmethod
    def get_user_certificates(user_id):
        """Get all certificates for a user"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        certificates = Certificate.objects(user_id=user)
        return list(certificates)
    
    @staticmethod
    def verify_certificate(verification_code):
        """Verify a certificate by its code"""
        try:
            certificate = Certificate.objects.get(verification_code=verification_code)
            return {
                'valid': True,
                'certificate': certificate.to_dict(),
                'user': certificate.user_id.to_dict() if hasattr(certificate.user_id, 'to_dict') else {},
                'learning_item': certificate.learning_item_id.to_dict()
            }
        except DoesNotExist:
            return {
                'valid': False,
                'message': 'Certificate not found'
            }
    
    @staticmethod
    def get_public_portfolio(user_id):
        """Get public portfolio for a user"""
        try:
            if isinstance(user_id, str):
                user = User.objects.get(id=user_id)
            else:
                user = user_id
        except DoesNotExist:
            raise ValueError("User not found")
        
        # Get public certificates
        public_certs = Certificate.objects(user_id=user, is_public=True)
        
        # Get completed learning items
        completed_items = LearningItem.objects(user_id=user, status='completed')
        
        return {
            'user_id': str(user.id),
            'certificates': [cert.to_dict() for cert in public_certs],
            'completed_items': [item.to_dict() for item in completed_items],
            'total_certificates': public_certs.count(),
            'total_completed': completed_items.count()
        }
