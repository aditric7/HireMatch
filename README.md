# 🎯 HireMatch

### NLP-Based Resume–Job Description Matching System

HireMatch is an NLP-based web application that analyzes a candidate's resume against a target job description and provides an interpretable match analysis.

Instead of only showing a similarity score, HireMatch identifies matching skills, missing skills, evidence from the resume, and generates a personalized preparation roadmap based on the detected skill gaps.

---

## 📌 Project Overview

Finding out whether a resume matches a particular job description can be difficult for students and job seekers.

HireMatch simplifies this process by comparing resume content with job requirements using Natural Language Processing (NLP) techniques.

The system:

- Extracts text from uploaded PDF resumes
- Compares the resume with a job description
- Calculates a TF-IDF based similarity score
- Detects relevant technical and soft skills
- Identifies matching and missing skills
- Provides evidence from the resume for detected skills
- Generates a personalized preparation roadmap

> **Note:** The similarity percentage is a text-similarity measure and is not a prediction of whether a candidate will be hired.

---

## 🎯 Problem Statement

Students and job seekers often find it difficult to determine whether their resume sufficiently matches a particular job description.

Traditional resume checking methods may require manually comparing skills and requirements.

HireMatch aims to provide a simple and explainable system that automatically compares a resume with a job description and highlights the candidate's skill gaps.

---

## 🚀 Objectives

The main objectives of HireMatch are:

1. To automatically extract text from PDF resumes.
2. To compare resume content with a target job description.
3. To calculate a resume-job similarity score using TF-IDF and cosine similarity.
4. To identify matching skills.
5. To identify missing skills required by the job description.
6. To provide evidence from the resume for detected skills.
7. To generate a job-specific preparation roadmap.
8. To provide an easy-to-use web interface for students and job seekers.

---

## ✨ Key Features

### 📄 PDF Resume Upload

Users can upload a resume in PDF format. HireMatch automatically extracts the text for analysis.

### 📊 Resume–Job Similarity

The system uses TF-IDF vectorization and cosine similarity to calculate how closely the resume text matches the job description.

### 🟢 Matching Skills

Skills detected in both the resume and job description are displayed as matching skills.

### 🔴 Missing Skills

Skills required by the job description but not detected in the resume are highlighted as skill gaps.

### 🔎 Resume Evidence

HireMatch provides evidence from the resume showing where detected skills appear.

### 📚 Personalized Preparation Roadmap

Based on missing skills, HireMatch generates a structured preparation roadmap with suggested topics and practice recommendations.

### 🎨 Interactive Web Interface

The application provides a clean Streamlit-based interface with separate sections for analysis, methodology, features, and project information.

---

## ⚙️ How HireMatch Works

The overall workflow is:

```text
                    Resume PDF
                        │
                        ▼
               PDF Text Extraction
                        │
                        ▼
                 Text Processing
                        │
                        ├──────────────┐
                        │              │
                        ▼              ▼
               Resume Text       Job Description
                        │              │
                        └──────┬───────┘
                               ▼
                       TF-IDF Vectorization
                               │
                               ▼
                      Cosine Similarity
                               │
                               ▼
                     Match Score
                               │
                               ▼
                       Skill Extraction
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
          Matching Skills             Missing Skills
                  │                         │
                  ▼                         ▼
          Resume Evidence          Skill Gap Analysis
                                            │
                                            ▼
                                  Preparation Roadmap