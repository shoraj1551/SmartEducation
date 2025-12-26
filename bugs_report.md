# Codebase Analysis Report

## Urls

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 1: `https://img.youtube.com/vi/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 2: `https://www.youtube-nocookie.com/embed/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 3: `https://player.vimeo.com/video/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 4: `https://img.youtube.com/vi/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 5: `https://youtube.com/watch?v=`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 6: `https://udemy.com/course/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\constants.py`: line 7: `https://coursera.org/learn/`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 16: `http://localhost`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_bookmark.py`: line 23: `https://en.wikipedia.org/wiki/Artificial_intelligence`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 151: `https://example.com/course`

## Secrets

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 14: `SECRET_KEY = os.getenv('SECRET_KEY',`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 14: `secret-key-change-in-production')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 15: `SECRET_KEY = os.getenv('JWT_SECRET_K`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 15: `secret-key-change-in-production')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 31: `PASSWORD = os.getenv('MAIL_PASSWORD')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 38: `TOKEN = os.getenv('TWILIO_AUTH_TOKE`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 47: `TOKEN_EXPIRES = timedelta(hours=24)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 55: `SECRET_KEY': cls.SECRET_KEY,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 56: `SECRET_KEY': cls.JWT_SECRET_KEY,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 58: `PASSWORD': cls.MAIL_PASSWORD,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 60: `TOKEN': cls.TWILIO_AUTH_TOKEN,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 9: `password_hash, check_password_hash`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 20: `password_hash = StringField(max_length`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 21: `password_history = ListField(StringFie`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 21: `password hashes`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 75: `password(self, password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 76: `password_hash = generate_password_hash`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 76: `password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 78: `password(self, password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 79: `password_hash(self.password_hash, pass`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 81: `password_in_history(self, password, co`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 82: `password matches any of the last N pas`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 83: `password_history:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 86: `passwords = self.password_history[-cou`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 86: `password_history) >= count else self.p`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 88: `passwords:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 90: `password_hash(old_hash, password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 97: `password_history(self, password_hash):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 98: `password hash to history, keeping only`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 99: `password_history:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 100: `password_history = []`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 102: `password_history.append(password_hash)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 104: `passwords`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 105: `password_history) > 3:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 106: `password_history = self.password_histo`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 161: `password_reset, account_deletion`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 408: `token = StringField(max_length=500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 408: `token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 409: `token = StringField(max_length=500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 409: `token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 410: `token_expires_at = DateTimeField()`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 14: `secrets": re.compile(r"(?i)(secret|k`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 14: `token|password)[^\n]{0,30}"),`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 41: `key = str(py_file)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 42: `key] = []`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 43: `key] = set()`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 47: `key].append(alias.name)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 52: `key].append(full)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 54: `key].add(node.id)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py`: line 25: `password_hash = bcrypt.hashpw('Passwor`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\debug_user_status.py`: line 30: `Password Hash: {'Yes' if user.password`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\debug_user_status.py`: line 44: `password or frontend.")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 35: `password = "SecurePassword123!"`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 41: `Password: {password}")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 49: `password': password`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 122: `password': password`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 133: `token = data.get('token')`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 134: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 135: `token returned.")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 139: `Token received: {token[:20]}...")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 145: `TOKEN / PROTECTED ROUTE`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 146: `Token)...")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 147: `token': token}`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 149: `token', json=t_payload)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 153: `Token is valid.")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 156: `Token verification failed: {data}")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 160: `token: {e}")`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_bookmark.py`: line 10: `token and user data`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_bookmark.py`: line 12: `password = 'Password123!'`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_bookmark.py`: line 13: `password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_bookmark.py`: line 15: `keys:', user_data.keys())`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_login.py`: line 9: `password = 'Password123!'`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\test_login.py`: line 12: `password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 38: `password("password123")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 40: `token = AuthService.generate_token(`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 41: `token}'}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 122: `password("pass123")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 125: `token = AuthService.generate_token(`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 127: `token}'})`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 41: `password_hash="hashed_password"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 20: `password_hash='hash').save()`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 20: `password_hash='hash').save()`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 20: `SECRET_KEY' in os.environ:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 21: `SECRET_KEY']`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 23: `key)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 36: `SECRET_KEY' in os.environ:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 37: `SECRET_KEY']`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 50: `SECRET_KEY', etc. We must patch the`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 52: `SECRET_KEY='test_key',`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 53: `SECRET_KEY='test_jwt',`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 55: `PASSWORD='pass',`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 57: `TOKEN='token',`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_flow.py`: line 24: `password_hash='hash'`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_limit.py`: line 27: `password_hash='hash'`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 37: `password_hash="hashed_password"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 3: `password_hash`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 5: `Password(unittest.TestCase):`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 6: `password_hashing(self):`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 8: `password("secret")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 10: `password_hash`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 12: `password("secret"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 13: `password("wrong"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 15: `password_history(self):`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 18: `password_hash("pass1")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 19: `password_hash("pass2")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 20: `password_hash("pass3")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 21: `password_hash("pass4")`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 23: `password_history(p1)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 24: `password_history(p2)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 25: `password_history(p3)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 26: `password_history), 3)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 28: `password_history(p4)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 29: `password_history), 3)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 30: `password_history)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 31: `password_history)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 33: `password_in_history`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 34: `password_in_history("pass4"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 35: `password_in_history("pass3"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 36: `password_in_history("pass2"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 37: `password_in_history("pass1")) # Expire`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 38: `password_in_history("pass99"))`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 19: `password_hash='hash').save()`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 20: `password_hash='hash').save()`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 19: `password_hash='hash').save()`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 47: `password']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 80: `password'],`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 210: `token = AuthService.generate_token(`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 215: `token': token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 250: `password"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 255: `password')]):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 256: `password are required'}), 400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 281: `password']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 302: `token': result['token']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 309: `password', methods=['POST'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 310: `password():`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 311: `password reset"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 319: `password reset`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 320: `password_reset(data['identifier'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 334: `password', methods=['POST'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 335: `password():`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 336: `password with OTP verification"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 341: `password']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 346: `password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 347: `password(`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 351: `password']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 363: `token', methods=['POST'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 364: `token():`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 365: `token"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 369: `token'):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 370: `token is required'}), 400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 372: `token(data['token'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 375: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 5: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 12: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 35: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 54: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 67: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 91: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 118: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 38: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 54: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 69: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 37: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 59: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 69: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 92: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 108: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 119: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 23: `Token auth manual verify for speed/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 24: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 25: `token and token.startswith('Bearer`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 26: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 27: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 28: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 29: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 86: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 87: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 145: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 146: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 16: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 17: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 18: `Token missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 20: `token.startswith('Bearer '): token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 20: `token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 21: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 22: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 26: `Token error'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 30: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 23: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 24: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 26: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 28: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 34: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 40: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 63: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 89: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 105: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 129: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 153: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 168: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 181: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 207: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 220: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 233: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 37: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 50: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 38: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 64: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 91: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 118: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 37: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 47: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 14: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 18: `token: return jsonify({'error': 'To`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 20: `token.startswith('Bearer '): token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 20: `token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 21: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 22: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 25: `Token error'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 29: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 39: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 53: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 67: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 12: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 15: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 16: `token: return jsonify({'error': 'To`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 18: `token.startswith('Bearer '): token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 18: `token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 19: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 20: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 23: `Token error'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 27: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 12: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 13: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 16: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 17: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 20: `token_payload(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 22: `Token is invalid or expired'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 112: `password/update', methods=['POST'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 114: `password():`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 115: `password with OTP verification"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 117: `password = data.get('current_password'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 118: `password = data.get('new_password')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 121: `password or not new_password:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 122: `passwords are required'}), 400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 124: `Password First (to prevent OTP spam/en`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 125: `password(current_password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 126: `password is incorrect'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 132: `password_change')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 142: `password_change') # user_id is implici`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 150: `password_change')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 156: `password(g.user.id, current_password,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 156: `password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 157: `Password updated successfully'}), 200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 14: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 18: `token: return jsonify({'error': 'To`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 20: `token.startswith('Bearer '): token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 20: `token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 21: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 22: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 25: `Token error'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 29: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 40: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 67: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 75: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 83: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 14: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 15: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 18: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 19: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 20: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 23: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 24: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 26: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 28: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 33: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 39: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 70: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 86: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 107: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 12: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 15: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 16: `token: return jsonify({'error': 'To`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 18: `token.startswith('Bearer '): token`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 18: `token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 19: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 20: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 23: `Token error'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 27: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 40: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 50: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 14: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 21: `token format`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 27: `Token is invalid or expired'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 42: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 50: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 69: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 88: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 94: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 122: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 126: `key 'profile_picture'.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 178: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 227: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 244: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 285: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 292: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 323: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 342: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 358: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 366: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 38: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 53: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 76: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 100: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 124: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 139: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 13: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 14: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 17: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 18: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 19: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 22: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 23: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 25: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 27: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 32: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 38: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 53: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 68: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 14: `token_required(f):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 15: `token for protected routes"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 18: `token = request.headers.get('Author`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 19: `token:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 20: `Token is missing'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 23: `token.startswith('Bearer '):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 24: `token = token[7:]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 26: `token(token)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 28: `token'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 33: `Token verification failed'}), 401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 38: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 48: `token_required`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 18: `secrets`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 22: `secrets.token_hex(12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 30: `password_hash': None  # Initialize to`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 30: `KeyError`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 89: `password_hash = pending_user['password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 103: `password_hash = pending_user['password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 114: `password, temp_user_id=None):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 128: `password_hash = bcrypt.hashpw(password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 135: `password_hash = password_hash`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 147: `password_hash=password_hash,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 203: `password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 204: `password (BUG-007 fix)"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 214: `password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 215: `password(password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 243: `secrets`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 244: `secrets.token_hex(16)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 246: `token with session_id`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 247: `token = AuthService.generate_token(`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 259: `token': token,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 264: `password_reset(identifier):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 265: `password reset via email or mobile"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 295: `password reset')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 300: `password reset')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 312: `password(user_id, email_otp, mobile_ot`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 312: `password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 313: `password with OTP verification"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 328: `password history - new password cannot`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 328: `passwords`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 329: `password_in_history(new_password, coun`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 330: `password cannot match your last 3 pass`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 330: `password."`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 332: `password to history before updating`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 333: `password_hash:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 334: `password_history(user.password_hash)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 336: `password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 337: `password(new_password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 340: `Password reset successfully"`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 361: `token(user_id, session_id=None):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 362: `token"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 365: `TOKEN_EXPIRES']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 370: `SECRET_KEY'], algorithm='HS256')`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 373: `token(token):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 374: `token and return user_id"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 376: `token, current_app.config['JWT_SECR`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 376: `KEY'], algorithms=['HS256'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 382: `token_payload(token):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 383: `token and return full payload"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 385: `token, current_app.config['JWT_SECR`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 385: `KEY'], algorithms=['HS256'])`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py`: line 18: `keywords = [`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py`: line 34: `keywords)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 55: `keys())`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 470: `key=lambda x: x['progress_percent`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py`: line 108: `key - placeholder implementation`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py`: line 123: `key - placeholder implementation`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py`: line 156: `token):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py`: line 169: `token):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 58: `PASSWORD'):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 111: `TOKEN'):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 124: `TOKEN']`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 241: `key=lambda x: x['days_wasted'], r`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 125: `key = (start_check_date + timedel`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 126: `key] = 0`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 130: `key = task.completed_at.date().is`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 131: `key in daily_effort:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 132: `key] += task.actual_duration_minu`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\review_service.py`: line 36: `key=daily_dist.get)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 109: `password_hash = "DELETED"`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 118: `password(user_id, current_password, ne`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 118: `password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 119: `password with validation"""`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 124: `password`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 125: `password(current_password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 126: `password is incorrect")`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 128: `password (length check for now, can ex`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 129: `password) < 8:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 130: `password must be at least 8 characters`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 133: `password_in_history(new_password):`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 134: `password cannot match recent passwords`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 137: `password_hash:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 138: `password_history(user.password_hash)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 140: `password(new_password)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 146: `password_change',`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 147: `Password updated successfully"`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 105: `key=lambda x: x[1])[0] if daily_b`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py`: line 43: `Key is present, we return`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py`: line 51: `key, else fallback to "Smart Mock`

## Numeric Literals

- `C:\Users\SHORAJ TOMER\SmartEducation\run.py`: line 7: `5000)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 19: `:27017/`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 29: `2525)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 42: `10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 44: `60)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py`: line 47: `=24)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 17: `=100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 18: `=120,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 19: `=15,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 20: `=255,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 21: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 25: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 35: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 36: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 37: `=20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 38: `=20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 40: `-001)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 41: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 42: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 43: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 44: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 45: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 46: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 49: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 51: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 53: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 54: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 55: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 58: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 63: `21)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 68: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 121: `-001)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 158: `=120)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 159: `=15)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 161: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 162: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 178: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 179: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 198: `=200,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 199: `=500,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 201: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 205: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 208: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 209: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 211: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 215: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 216: `-100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 217: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 218: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 252: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 253: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 256: `=255,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 264: `=200,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 268: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 289: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 290: `=100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 291: `=255)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 293: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 328: `=300,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 332: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 333: `=500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 334: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 337: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 361: `=50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 362: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 392: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 403: `=100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 404: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 408: `=500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 409: `=500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 415: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 459: `=20.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 459: `20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 462: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 489: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 500: `10}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 510: `=300,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 512: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 526: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 530: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 626: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 677: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 684: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 714: `11:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 725: `20}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 770: `=20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 809: `=100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 845: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 862: `12:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py`: line 872: `10,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\version.py`: line 21: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\version.py`: line 21: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\version.py`: line 22: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py`: line 14: `,30}`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py`: line 10: `:27017/`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py`: line 14: `'9999999999'`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 16: `:5000/`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 19: `=10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 26: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 28: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 34: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 55: `201:`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 107: `200:`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 129: `200:`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 139: `:20]`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 152: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 163: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py`: line 165: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 3: `19)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 4: `(11)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 4: `(12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 4: `(13)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 4: `(15)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 36: `"9998887777"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 45: `11:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 49: `200)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 60: `200)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 68: `12:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 84: `201)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 94: `200)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 104: `13:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 108: `200)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 120: `"1112223333"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 128: `200)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 136: `15:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 144: `"2025-`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 144: `-01"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py`: line 145: `=30,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 40: `"1234567890"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 109: `[80,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 109: `50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 109: `20]`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 114: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 128: `80)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 129: `50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 130: `20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 136: `80%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 139: `80)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 141: `20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py`: line 144: `20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 18: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 18: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 20: `'555{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 23: `600}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 27: `(21`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 28: `15`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 29: `=21)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 31: `21`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_breakdown.py`: line 34: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 18: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 18: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 20: `'888{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 28: `=30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 31: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 36: `45}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 40: `30}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 45: `15}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 51: `45)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_commitment.py`: line 51: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py`: line 58: `'123'`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 17: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 18: `(500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 19: `(2000/`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 20: `(2000)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `10:`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `/500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `/500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `81`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 21: `40500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 24: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 25: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 25: `500.`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 26: `500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 27: `2000`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 28: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 28: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 28: `2000.`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py`: line 29: `2000)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_flow.py`: line 16: `(10000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_flow.py`: line 16: `99999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_flow.py`: line 18: `'99999{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_limit.py`: line 16: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_limit.py`: line 16: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_limit.py`: line 17: `'123456{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 36: `"1234567890"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 53: `600`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 62: `600)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 150: `100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 170: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 174: `50%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 175: `50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 176: `50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 177: `50.`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 180: `100%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 181: `100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 182: `100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 211: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 218: `20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 227: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py`: line 227: `20`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 7: `"1234567890"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py`: line 16: `"0987654321"`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 17: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 17: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 19: `'666{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 30: `=120,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 35: `75)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 36: `*40=`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 36: `*40=`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 36: `(10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 36: `82`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 38: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 44: `=60)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 45: `=300,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 50: `50)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 51: `*40=`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 51: `*40=`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 51: `25`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 59: `=15,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 59: `15`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 64: `~50-`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 65: `*40=`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 65: `(20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_priority.py`: line 65: `52`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 18: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 18: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 20: `'777{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 22: `50`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 22: `3000`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 26: `3000`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 26: `50`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 29: `(50`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 30: `(20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 30: `(3000*`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 30: `/60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 33: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 33: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 33: `300`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 33: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 34: `=10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 36: `(10`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 36: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 40: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 47: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 47: `90`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 47: `5400`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 47: `(90`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 47: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 48: `=60)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 50: `(60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 50: `90`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_reality_check.py`: line 54: `90`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 17: `(1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 17: `9999)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 19: `'444{`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 27: `=100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 30: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 36: `=60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 37: `=60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 47: `=60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 50: `(30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 56: `=30,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 57: `=60`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 63: `=1000,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 68: `=10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 69: `=100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 79: `60+`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 79: `+30`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 79: `92`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 79: `~13`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 86: `1000`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 86: `20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 86: `1200`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 87: `~13`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 88: `1200`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 88: `13`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 88: `~92`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 89: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_truth.py`: line 90: `~82`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 11: `-002)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 15: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 15: `12`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 15: `91)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 25: `10:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 28: `12:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 29: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 30: `'91'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 34: `91`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 36: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 36: `9876543210)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 36: `12`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 36: `919876543210)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 44: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 50: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 52: `-008`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 59: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 68: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 70: `-002)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 73: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 85: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 89: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 103: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 112: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 115: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 124: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 128: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 132: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 134: `-002)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 138: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 151: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 154: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 166: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 176: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 178: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 181: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 194: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 197: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 207: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 216: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 219: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 230: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 240: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 242: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 245: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 256: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 260: `-002)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 285: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 295: `403`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 303: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 306: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 317: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 323: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 328: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 331: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 344: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 355: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 357: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 360: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 370: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 375: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 382: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py`: line 385: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 17: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 31: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 32: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 39: `20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 48: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 51: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 63: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 64: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 73: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 87: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 88: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 97: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 115: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 123: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 127: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 139: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py`: line 141: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 42: `=14,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 45: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 48: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 50: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 60: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 63: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 65: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 78: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 81: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py`: line 83: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 43: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 51: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 54: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 56: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 64: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 66: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 75: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 85: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 87: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 89: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 101: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 103: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 105: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 113: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 115: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 127: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 132: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 142: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 144: `8601'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 144: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 151: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py`: line 154: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 29: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 56: `=23,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py`: line 56: `=59)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 30: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 42: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 45: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 77: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 80: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 88: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 95: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 103: `60`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 126: `10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 126: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 128: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 136: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 139: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 147: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 153: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 158: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py`: line 160: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 18: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 22: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 26: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 35: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py`: line 37: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 28: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 34: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 47: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 54: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 57: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 59: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 82: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 85: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 96: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 98: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 101: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 112: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 120: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 123: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 125: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 136: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 144: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 147: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 149: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 159: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 162: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 164: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 174: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 177: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 188: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 200: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 203: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 213: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 216: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 226: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 229: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 240: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 245: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 245: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py`: line 250: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py`: line 59: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 45: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 47: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 58: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py`: line 60: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 2: `10:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 45: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 55: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 58: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 60: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 71: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 82: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 85: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 87: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 98: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 109: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 112: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 114: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 127: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 130: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 132: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 141: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 141: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 144: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 153: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 156: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py`: line 158: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 42: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 44: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 61: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 67: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py`: line 69: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 3: `12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 18: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 22: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 25: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 34: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 36: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 48: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 50: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 62: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 64: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 83: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py`: line 85: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 3: `15)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 16: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 20: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 23: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 32: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py`: line 34: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 14: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 22: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 33: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 46: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 48: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 58: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 62: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 63: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 69: `10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 71: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 81: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 90: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 92: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 102: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 106: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 108: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 110: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 122: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 126: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 136: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 138: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 152: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 157: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 159: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py`: line 161: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 3: `13)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 18: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 22: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 25: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 35: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 36: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 37: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 63: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 64: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 71: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 72: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 79: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 80: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 89: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py`: line 90: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 20: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 28: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 33: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 46: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 50: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 61: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 64: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 66: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 79: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 82: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 98: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 101: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 103: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 114: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 119: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 130: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 133: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py`: line 135: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 3: `11)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 16: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 20: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 23: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 35: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 37: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 45: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 47: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 55: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py`: line 57: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 33: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 36: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 45: `20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 55: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 65: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 66: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 99: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 119: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 133: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 137: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 173: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 175: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 180: `-001)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 183: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 185: `-001)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 224: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 249: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 282: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 298: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 305: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 306: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 318: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 320: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 329: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 339: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py`: line 371: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 44: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 47: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 49: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 60: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 67: `201`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 70: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 72: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 83: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 91: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 94: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 96: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 107: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 115: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 118: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 120: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 130: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 133: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 135: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 146: `400`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 153: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py`: line 156: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 19: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 27: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 32: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 44: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 47: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 49: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 59: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 62: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 64: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 75: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 78: `404`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py`: line 80: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 20: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 28: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 33: `401`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 43: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 45: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 53: `200`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py`: line 55: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py`: line 3: `13)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py`: line 34: `1000`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py`: line 78: `50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py`: line 79: `100%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py`: line 79: `100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py`: line 80: `150,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\activity_service.py`: line 27: `=20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 22: `(12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 204: `-007`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py`: line 244: `(16)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py`: line 60: `.25`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py`: line 101: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py`: line 109: `=20)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 12: `240`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 14: `14`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 23: `=21)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 39: `21`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 40: `(22)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py`: line 73: `15:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py`: line 65: `+00:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py`: line 267: `24`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py`: line 269: `48`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py`: line 133: `=30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py`: line 166: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 11: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 17: `500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 19: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 20: `2000`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 21: `4500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 24: `500)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 30: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 33: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 74: `500`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 80: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 80: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 88: `(100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 98: `(10,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 99: `(20,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 100: `(30,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 101: `(40,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 102: `(50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py`: line 103: `(100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 230: `100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 259: `100%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 260: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 463: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py`: line 482: `100%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py`: line 114: `600,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 65: `.98,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 68: `45,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 79: `.95,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 82: `100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 93: `.82,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 98: `'12'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 107: `.91,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 110: `12,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 112: `/12'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 115: `18`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 119: `18.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 121: `.88,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 135: `.96,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 138: `67,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py`: line 140: `'432'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 13: `11}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 13: `11`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 14: `17}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 15: `19,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 56: `19`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 60: `19`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py`: line 60: `19`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 59: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 61: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 66: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 81: `#666;`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 82: `#666;`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 84: `#999;`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 84: `2025`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 112: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 114: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 119: `*60}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 153: `123456`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 154: `'123456'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 168: `123456`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py`: line 169: `'123456'`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 13: `-100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 16: `(40%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 17: `(40%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 18: `(20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 21: `40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 23: `100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 25: `40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 27: `40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 35: `14:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 37: `30:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 41: `40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 43: `20`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 45: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 48: `30:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 49: `20`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 50: `60:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 51: `15`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 52: `180:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py`: line 53: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 2: `10:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 11: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 19: `=70)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 63: `=50,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 104: `70)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 152: `100%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 155: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 176: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py`: line 210: `:12]`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 103: `100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 105: `(100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 105: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 121: `100:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 150: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 169: `-100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 173: `50.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 180: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 182: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 183: `(100.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 190: `90:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 192: `75:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 194: `50:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 196: `25:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 202: `14:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 208: `=30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 257: `30:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 263: `=30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 290: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py`: line 296: `(100,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 16: `20%`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 79: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 80: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 81: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 89: `/60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 90: `/60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 94: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 95: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 96: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 110: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 114: `=30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 116: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 124: `(31)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py`: line 168: `9999`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py`: line 3: `12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py`: line 35: `.08`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py`: line 35: `.02)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py`: line 38: `.08`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py`: line 38: `.02)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\review_service.py`: line 51: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\review_service.py`: line 56: `60,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\search_service.py`: line 3: `15)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py`: line 42: `=10)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 15: `20.`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 16: `15`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 16: `15`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 17: `120`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 18: `45`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 18: `45`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 60: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 118: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 213: `20:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 215: `70:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 225: `90:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 227: `80:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 237: `100`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py`: line 313: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 3: `11)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 24: `(20:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 25: `20:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 43: `10:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 47: `=23,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 47: `=59)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 62: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 64: `15:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 80: `12`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py`: line 81: `=12)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\video_guard_service.py`: line 22: `{11}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 97: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 126: `80:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 133: `60:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 150: `60:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 157: `30:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 161: `60+`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 212: `70:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 220: `210:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 220: `30`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 223: `(30+`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 252: `(40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 253: `100)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 253: `40`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 255: `(30`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 255: `420`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 255: `(60`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 256: `(30,`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 256: `420)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 256: `30)`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 259: `(20`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 260: `20`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 263: `(10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 265: `10`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 270: `90:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 272: `80:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 274: `70:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py`: line 276: `60:`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py`: line 23: `{11}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py`: line 32: `{11}`

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py`: line 57: `15,`

## Unused Imports

- `C:\Users\SHORAJ TOMER\SmartEducation\qa_runner.py` imports `tests.qa_uat_intelligence.TestIntelligenceLayer` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\test_imports.py` imports `bson.ObjectId` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\test_imports.py` imports `app.services.library_service.LibraryService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\test_imports.py` imports `app.routes.user_routes.user_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\test_import_config.py` imports `app.config` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py` imports `datetime.timedelta` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\config.py` imports `dotenv.load_dotenv` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.Document` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.StringField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.BooleanField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.DateTimeField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.IntField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.ReferenceField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.FloatField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.ListField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `mongoengine.DictField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `werkzeug.security.generate_password_hash` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\models.py` imports `werkzeug.security.check_password_hash` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `flask.Flask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `flask_cors.CORS` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `flask_session.Session` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `config.Config` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `services.otp_service.mail` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `os` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `mongoengine.connect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.auth_routes.auth_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.user_routes.user_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.bookmark_routes.bookmark_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.inbox_routes.inbox_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.commitment_routes.commitment_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.priority_routes.priority_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.dashboard_routes.dashboard_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.focus_routes.focus_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.reality_routes.reality_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.wellness_routes.wellness_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.gamification_routes.gamification_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.security_routes.security_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.recall_routes.recall_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.trigger_routes.trigger_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.social_routes.social_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.search_routes.search_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.preference_routes.preference_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\__init__.py` imports `routes.main_routes.main_bp` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py` imports `os` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py` imports `json` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\analyze_codebase.py` imports `pathlib.Path` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py` imports `dotenv.load_dotenv` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py` imports `mongoengine.connect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\create_test_user.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\e2e_auth_test.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\find_missing_connections.py` imports `os` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\scripts\find_missing_connections.py` imports `pathlib.Path` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `json` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.create_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.TriggerRule` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.Notification` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.Flashcard` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.AccountabilityPartner` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\qa_uat_intelligence.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `mongoengine.connect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `mongoengine.disconnect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.services.inbox_service.InboxService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_blocking_logic.py` imports `app.services.inbox_service.InboxService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_config_validation.py` imports `app.config.Config` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_gamification.py` imports `app.services.gamification_service.GamificationService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_limit.py` imports `mongoengine` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `datetime.timedelta` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `mongoengine.connect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `mongoengine.disconnect` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_inbox_service.py` imports `app.services.inbox_service.InboxService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_models_password.py` imports `werkzeug.security.generate_password_hash` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_srs.py` imports `app.services.recall_service.RecallService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_srs.py` imports `app.models.Flashcard` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_srs.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_srs.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\tests\test_srs.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\auth_routes.py` imports `app.services.activity_service.ActivityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.routes.user_routes.token_required` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.services.bookmark_service.BookmarkService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.models.Bookmark` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.services.library_service.LibraryService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.services.library_service.LibraryService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.services.otp_service.OTPService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\bookmark_routes.py` imports `app.services.otp_service.OTPService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `app.services.burnout_service.BurnoutDetectionService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\burnout_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `app.services.commitment_service.CommitmentService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\commitment_routes.py` imports `app.services.reality_service.RealityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `app.services.priority_service.PriorityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\dashboard_routes.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `flask.render_template` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.models.FocusSession` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.services.video_guard_service.VideoGuardService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\focus_routes.py` imports `app.services.gamification_service.GamificationService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `app.services.gamification_service.GamificationService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\gamification_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `app.services.inbox_service.InboxService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\inbox_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\main_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\main_routes.py` imports `flask.render_template` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `flask.g` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `app.routes.security_routes.login_required` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\preference_routes.py` imports `app.services.orchestrator_service.OrchestratorService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `app.services.priority_service.PriorityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\priority_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `app.services.proof_of_learning_service.ProofOfLearningService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\proof_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `app.services.reality_service.RealityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\reality_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `app.services.recall_service.RecallService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `app.models.Flashcard` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\recall_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `app.services.search_service.SearchService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\search_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `flask.g` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `app.services.security_service.SecurityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\security_routes.py` imports `bson.ObjectId` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `app.services.accountability_service.AccountabilityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `app.models.AccountabilityPartner` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\social_routes.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `app.services.task_generator_service.TaskGeneratorService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\task_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `app.services.trigger_service.TriggerService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\trigger_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `flask.current_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.models.Schedule` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.services.activity_service.ActivityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `bson.ObjectId` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.models.Activity` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `werkzeug.utils.secure_filename` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.services.achievement_service.AchievementService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\user_routes.py` imports `app.services.achievement_service.AchievementService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `app.services.video_guard_service.VideoGuardService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\video_guard_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `app.services.weekly_review_service.WeeklyReviewService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\weekly_review_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `flask.Blueprint` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `flask.jsonify` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `flask.request` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `app.services.burnout_service.BurnoutService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `app.services.review_service.WeeklyReviewService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\routes\wellness_routes.py` imports `functools.wraps` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py` imports `app.models.AccountabilityPartner` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py` imports `app.models.Notification` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\accountability_service.py` imports `app.models.Commitment` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.models.Achievement` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.models.UserAchievement` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.models.Activity` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.services.activity_service.ActivityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `json` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\achievement_service.py` imports `app.models.Bookmark` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\activity_service.py` imports `app.models.Activity` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `flask.current_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `mongoengine.queryset.visitor.Q` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `app.models.UserSession` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `app.services.otp_service.OTPService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `flask.session` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `flask.session` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\auth_service.py` imports `flask.session` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py` imports `json` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py` imports `app.models.Bookmark` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\bookmark_service.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\breakdown_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\breakdown_service.py` imports `app.models.Commitment` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\breakdown_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\burnout_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.models.Commitment` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.models.CommitmentViolation` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.models.AccountabilityPartner` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.services.reality_service.RealityService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\commitment_service.py` imports `app.services.breakdown_service.AutoBreakdownService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py` imports `app.models.FocusSession` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\focus_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\gamification_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `app.models.ContentSource` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `mongoengine.errors.ValidationError` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `app.services.adapters.factory.AdapterFactory` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\inbox_service.py` imports `app.models.Bookmark` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py` imports `datetime.datetime` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py` imports `app.models.ContentSource` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\integration_service.py` imports `app.constants.YOUTUBE_MAXRES_THUMBNAIL_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `random` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `flask.current_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `werkzeug.utils.secure_filename` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `app.models.Bookmark` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `bson.ObjectId` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `app.constants.YOUTUBE_WATCH_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `app.constants.UDEMY_COURSE_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\library_service.py` imports `app.constants.COURSERA_LEARN_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\orchestrator_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py` imports `flask.current_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py` imports `flask_mail.Mail` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py` imports `flask_mail.Message` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py` imports `twilio.rest.Client` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\otp_service.py` imports `app.models.OTP` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\priority_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.Document` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.ReferenceField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.StringField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.IntField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.BooleanField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.DateTimeField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.ListField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.DictField` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\proof_of_learning_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_metrics_service.py` imports `math` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `app.models.Commitment` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\reality_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py` imports `app.models.Flashcard` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\recall_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\review_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\review_service.py` imports `calendar` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\search_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\search_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\search_service.py` imports `app.models.Flashcard` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\search_service.py` imports `mongoengine.queryset.visitor.Q` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `app.models.UserSession` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `app.models.Activity` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `app.models.OTP` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `app.services.auth_service.AuthService` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\security_service.py` imports `flask.current_app` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `app.models.LearningPlan` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\task_generator_service.py` imports `math` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py` imports `app.models.Notification` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\trigger_service.py` imports `app.models.Commitment` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\video_guard_service.py` imports `app.constants.YOUTUBE_EMBED_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\video_guard_service.py` imports `app.constants.VIMEO_EMBED_URL_TEMPLATE` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `app.models.LearningItem` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `app.models.DailyTask` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `app.models.FocusSession` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `app.models.CommitmentViolation` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `app.models.User` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\weekly_review_service.py` imports `mongoengine.errors.DoesNotExist` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\base.py` imports `abc.ABC` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\base.py` imports `abc.abstractmethod` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\base.py` imports `typing.Dict` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\base.py` imports `typing.Any` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\base.py` imports `typing.Optional` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\factory.py` imports `typing.Optional` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\factory.py` imports `base.BaseAdapter` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\factory.py` imports `youtube.YouTubeAdapter` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `requests` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `typing.Dict` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `typing.Any` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `typing.Optional` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `base.BaseAdapter` but never uses it

- `C:\Users\SHORAJ TOMER\SmartEducation\app\services\adapters\youtube.py` imports `app.constants.YOUTUBE_THUMBNAIL_URL_TEMPLATE` but never uses it

## Config Hardcoded Values

- None found
