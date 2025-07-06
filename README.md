

# 🛡️ Supply Chain Security Platform

A real-time software dependency risk monitoring and anomaly detection platform using Kafka, Flink, Neo4j, Hive, Spark, and GNN.

## 📌 Project Summary

This project builds an end-to-end data engineering platform to track, analyze, and predict anomalous behaviors in the software supply chain. It ingests GitHub/NPM project dependency data, performs real-time anomaly detection with Flink, constructs a dynamic dependency graph with Neo4j, executes OLAP queries in Hive via Spark, and uses Graph Neural Networks to forecast potential risks. A REST API and a Streamlit dashboard enable interactive exploration of the graph and risk insights.

## ⚙️ Architecture Overview

![architecture](docs/architecture.png)

## 💡 Key Features

- Real-time dependency anomaly detection using Flink CEP
- Dynamic graph database of projects, libraries, versions, maintainers, and events in Neo4j
- Batch feature extraction and risk scoring using Hive + Spark
- Graph embedding and GNN-based classification of risky libraries
- REST API with FastAPI and visual dashboard with Streamlit

## 🚀 Quick Start

```bash
docker compose -f docker-compose.yml up -d
```

Ensure you set up a `.env` file with a valid GitHub token for crawling.

## 🧱 Project Structure

| Folder             | Description |
|--------------------|-------------|
| `data_ingestion/`  | GitHub/NPM crawlers and Kafka producers |
| `stream_processing/` | Flink CEP logic for real-time detection |
| `graph_model/`     | Neo4j graph loader and schema definition |
| `batch_analysis/`  | Hive schema, Spark analysis, risk scoring |
| `embedding/`       | Graph embedding and GNN classification |
| `api_service/`     | FastAPI server and API endpoints |
| `dashboard/`       | Streamlit-based visualization dashboard |
| `dags/`            | Airflow DAGs for scheduled tasks |
| `docs/`            | Architecture diagrams and project notes |

## ✨ Sample Kafka Message Format

```json
{
  "repo": "psf/requests",
  "dependencies": ["urllib3", "chardet", "certifi"],
  "timestamp": "2025-10-01T12:00:00Z",
  "language": "Python"
}
```

## 🧪 Tech Stack

- Kafka, Flink, Neo4j, Hive, HDFS, Spark
- Python (data ingestion, GNN)
- FastAPI, Streamlit, Docker Compose
