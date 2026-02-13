#importar imagen base de pyhton 3.12 slim
FROM python:3.12-slim

#crear en el contenedor una carpeta de trabajo 
WORKDIR /app

#Copiar los requirimientos al contenedor
COPY requirements.txt .

#Instalamos las dependencias 
RUN pip install --no-cache-dir -r requirements.txt

#Copiar el código del servidor
COPY ./app ./app

#Exponer el puerto trabajo
EXPOSE 5000

#comando que se jecura para levantar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
