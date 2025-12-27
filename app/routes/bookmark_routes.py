"""
Bookmark API routes for SmartEducation
"""
from flask import Blueprint, request, jsonify
from app.routes.user_routes import token_required
from app.services.bookmark_service import BookmarkService
from app.models import Bookmark

bookmark_bp = Blueprint('bookmark', __name__, url_prefix='/api/bookmarks')

@bookmark_bp.route('', methods=['POST'])
@token_required
def add_bookmark(current_user):
    """Add a new bookmark"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
        
    bookmark, message = BookmarkService.add_bookmark(
        current_user.id,
        data['url'],
        data.get('title'),
        data.get('description'),
        data.get('tags')
    )
    
    if bookmark:
        return jsonify({
            'message': message,
            'bookmark': bookmark.to_dict()
        }), 201
    return jsonify({'error': message}), 500

@bookmark_bp.route('', methods=['GET'])
@token_required
def get_bookmarks(current_user):
    """Get paginated bookmarks for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    bookmarks, total = BookmarkService.get_bookmarks(current_user.email, page, per_page)
    
    return jsonify({
        'bookmarks': [b.to_dict() for b in bookmarks],
        'total': total,
        'page': page,
        'per_page': per_page
    }), 200



@bookmark_bp.route('/sync', methods=['POST'])
@token_required
def sync_library(current_user):
    """Simulate syncing from external sources"""
    # Import inside function to avoid circular imports if any, though likely safe at top
    from app.services.library_service import LibraryService
    
    success, message = LibraryService.simulate_sync(current_user.id, current_user.email)
    
    if success:
        return jsonify({'message': message}), 200
    return jsonify({'error': message}), 400

@bookmark_bp.route('/upload', methods=['POST'])
@token_required
def upload_book(current_user):
    """Handle manual book upload"""
    from app.services.library_service import LibraryService
    
    files = request.files.getlist('file')
    if not files or len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400

    if len(files) > 5:
        return jsonify({'error': 'Maximum 5 files allowed per upload'}), 400

    total_size = sum(f.content_length or 0 for f in files) 
    # content_length might not be set by all clients, usually need to read/seek
    # Simplified check: we'll check individual processing or trust client side mostly, 
    # but strictly we can check f.seek(0, os.SEEK_END)
    
    # Let's count successes
    uploaded_count = 0
    errors = []
    
    title_base = request.form.get('title', '')
    topic = request.form.get('topic', 'General')
    
    for i, file in enumerate(files):
        # Infer title for multiple files if generic
        current_title = title_base
        if len(files) > 1 and title_base:
            current_title = f"{title_base} ({i+1})"
        elif not title_base:
            current_title = file.filename
            
        success, message = LibraryService.handle_manual_upload(
            current_user.id,
            file,
            current_title,
            topic
        )
        if success:
            uploaded_count += 1
        else:
            errors.append(f"{file.filename}: {message}")
            
    if uploaded_count > 0:
        msg = f"Successfully uploaded {uploaded_count} files."
        if errors:
            msg += f" Failed: {', '.join(errors)}"
        return jsonify({'message': msg}), 201
        
    return jsonify({'error': f"Upload failed. {', '.join(errors)}"}), 400

@bookmark_bp.route('/<bookmark_id>/delete-otp', methods=['POST'])
@token_required
def request_delete_otp(current_user, bookmark_id):
    """Request OTP for bookmark deletion"""
    # Verify bookmark ownership
    bookmark = Bookmark.objects(id=bookmark_id, user=current_user).first()
    if not bookmark:
        return jsonify({'error': 'Resource not found'}), 404
        
    from app.services.otp_service import OTPService
    OTPService.create_otp(current_user.id, 'deletion', f'delete_{bookmark_id}')
    
    # Send email (mocked in service if config missing)
    # Ideally we'd look up the OTP here to send it via email service,
    # but the service handles creation and sending logic usually.
    # Here checking the service implementation: create_otp just creates.
    # We need to send it.
    
    # Re-reading OTPService from previous view: 
    # create_otp returns otp object.
    # send_email_otp takes (email, code, purpose).
    
    otp = OTPService.create_otp(current_user.id, 'deletion', f'delete_{bookmark_id}')
    OTPService.send_email_otp(current_user.email, otp.otp_code, 'Resource Deletion')
    
    return jsonify({'message': 'OTP sent to your email'}), 200

@bookmark_bp.route('/<bookmark_id>/confirm', methods=['DELETE'])
@token_required
def confirm_delete(current_user, bookmark_id):
    """Delete bookmark with OTP verification"""
    data = request.get_json()
    if not data or 'otp' not in data:
        return jsonify({'error': 'OTP is required'}), 400
        
    bookmark = Bookmark.objects(id=bookmark_id, user=current_user).first()
    if not bookmark:
        return jsonify({'error': 'Resource not found'}), 404
        
    from app.services.otp_service import OTPService
    success, message = OTPService.verify_otp(
        current_user.id, 
        data['otp'], 
        'deletion', 
        f'delete_{bookmark_id}'
    )
    
    if success:
        bookmark.delete()
        return jsonify({'message': 'Resource deleted successfully'}), 200
        
    return jsonify({'error': message}), 400
