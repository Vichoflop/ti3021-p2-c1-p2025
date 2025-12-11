import bcrypt

#paso 1 pedir contraseña
incoming_password = input("Ingrese su contraseña: ").encode("UTF-8")

#paso 2 generar un salt
salt = bcrypt.gensalt(rounds= 12)

#paso 3 hashear la contraseña con el salt
hashed_password = bcrypt.hashpw(incoming_password, salt)
print(hashed_password)

#paso 4 pedir nuevamente la contraseña
confirm_password = input("Ingrese nuevamente la contraseña: ").encode("UTF-8")

#paso 5 verificar si la contraseña corresponde
if bcrypt.checkpw(confirm_password, hashed_password):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")


