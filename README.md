ne pas oublier :
-tests

pour compiler :
 pyinstaller --onefile --name "SwaggerChecker" --add-data "config/projet_validation_rules.json;config" --add-data "C:\Users\lucas\innovation_enedis\swagger-validator\venv\Lib\site-packages\openapi_spec_validator\resources\schemas\v3.1\schema.json;openapi_spec_validator/resources/schemas/v3.1" main.py