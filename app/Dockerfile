# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos (requirements.txt) a la imagen
COPY requirements.txt .

# Instala las bibliotecas necesarias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
RUN pip install params
RUN pip install -U langchain-community

# Copia el resto de la aplicación al contenedor
COPY . .

# Expone el puerto para Flask
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"]