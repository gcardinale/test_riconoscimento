#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

FROM python:3.9 AS python
WORKDIR /src

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["STT_Application/STT_Application.csproj", "STT_Application/"]
RUN dotnet restore "./STT_Application/./STT_Application.csproj"

#COPY . .
WORKDIR "/src/STT_Application"
RUN dotnet build "./STT_Application.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./STT_Application.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Installazione di Python
USER root
RUN apt-get update -y && apt-get install -y python3 python3-pip
RUN pip3 install pythonnet
USER app

ENV PYTHONNET_PYDLL=/usr/bin/python3

# Configura la variabile d'ambiente PYTHONNET_PYDLL
# ENV PYTHONNET_PYDLL=/usr/lib/libpython3.9.so.1.0

ENTRYPOINT ["dotnet", "STT_Application.dll"]