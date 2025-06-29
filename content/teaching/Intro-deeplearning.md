---
title: "Introduction to deep learning"
date: 2023-09-01
draft: false
course_code: ""
semester: "Fall"
year: "2023"
level: "Undergraduate"
image: "/images/courses/Intro_Java.png"
summary: "An introduction to the programming language Java."
# credits: 3
# students: 45
# instructor: "Dr. John Smith"
# department: "Computer Science"
university: "Georgia Institute of Technology"
location: "Klaus Advanced Computing Building, Room 1443"
# schedule: "Tuesday & Thursday, 3:30-4:45 PM"
# office_hours: "Wednesdays 2:00-4:00 PM or by appointment"
prerequisites: 
  - "CS 3600 - Introduction to Artificial Intelligence"
  - "MATH 2552 - Differential Equations"
  - "STAT 3770 - Statistical Methods"
# textbooks:
#   - title: "Deep Learning"
#     authors: "Ian Goodfellow, Yoshua Bengio, Aaron Courville"
#     isbn: "978-0262035613"
#     required: true
#   - title: "Pattern Recognition and Machine Learning"
#     authors: "Christopher Bishop"
#     isbn: "978-0387310732"
#     required: false
image: "/images/courses/cs7643-neural-networks.jpg"
syllabus: "/files/syllabi/cs7643-fall2024-syllabus.pdf"
course_website: "https://canvas.gatech.edu/courses/cs7643"
summary: "An advanced graduate course covering state-of-the-art machine learning algorithms, with emphasis on deep learning architectures, optimization techniques, and real-world applications in computer vision and natural language processing."
tags:
  - "Machine Learning"
  - "Deep Learning"
  - "Neural Networks"
  - "Artificial Intelligence"
  - "Computer Vision"
  - "NLP"
  - "Graduate Course"
learning_objectives:
  - "Understand theoretical foundations of deep learning"
  - "Implement neural network architectures from scratch"
  - "Apply deep learning to computer vision problems"
  - "Design and train models for natural language processing"
  - "Evaluate and optimize model performance"
# grading:
#   homework: 40
#   midterm: 20
#   final_project: 30
#   participation: 10
tools_software:
  - "Python 3.8+"
  - "TensorFlow 2.x"
  - "PyTorch"
  - "Jupyter Notebooks"
  - "Google Colab"
  - "Git/GitHub"
# assignments:
#   - name: "Neural Network Fundamentals"
#     weight: 10
#     due_date: "2024-09-15"
#   - name: "Convolutional Neural Networks"
#     weight: 15
#     due_date: "2024-10-01"
#   - name: "Recurrent Neural Networks and LSTMs"
#     weight: 15
#     due_date: "2024-10-22"
# projects:
#   - name: "Deep Learning for Medical Image Analysis"
#     description: "Team project applying CNNs to medical imaging data"
#     team_size: "3-4 students"
#     deliverables: "Code, report, presentation"
# final_exam_date: "2024-12-10"
# final_exam_time: "2:50-5:40 PM"
# course_policies:
#   attendance: "Required for all lectures and labs"
#   late_policy: "10% penalty per day late, maximum 3 days"
#   collaboration: "Encouraged for learning, individual work for submissions"
# accessibility: "Accommodations available through ADAPTS office"
# lastmod: 2024-08-25
# featured: true
# weight: 1
---

## Course Description

This advanced graduate course provides comprehensive coverage of modern machine learning techniques with a particular emphasis on deep learning methodologies. Students will explore the mathematical foundations, implementation details, and practical applications of neural networks in various domains including computer vision, natural language processing, and reinforcement learning.

The course combines theoretical understanding with hands-on implementation, requiring students to build neural networks from scratch and apply state-of-the-art architectures to real-world problems. By the end of the course, students will have developed the expertise to design, implement, and deploy deep learning solutions for complex computational challenges.



{{< figure src=/images/courses/Intro_Java.png 
           alt="Neural ODE Architecture" 
           caption="Overview of the Neural ODE architecture for disease progression modeling. The network learns continuous dynamics from sparse clinical observations."
           numbered="true"
           number="1" >}}

<div class="equation-annotation">
<strong>Multi-component Model (Equation 2):</strong>
<ul>
<li><strong>$h_{\text{retinal}}(t)$:</strong> Retinal structural changes (thickness, volume)</li>
<li><strong>$h_{\text{vascular}}(t)$:</strong> Vascular health indicators (density, perfusion)</li>
<li><strong>$h_{\text{metabolic}}(t)$:</strong> Metabolic markers (glucose, HbA1c levels)</li>
<li><strong>$f_i(\cdot)$:</strong> Component-specific neural networks capturing biological interactions</li>
</ul>
</div>


## Course Objectives

Upon successful completion of this course, students will be able to:

1. **Theoretical Foundation**: Understand the mathematical principles underlying deep learning, including backpropagation, gradient descent optimization, and regularization techniques.

2. **Practical Implementation**: Implement various neural network architectures including feedforward networks, convolutional neural networks (CNNs), and recurrent neural networks (RNNs) using modern frameworks.

3. **Computer Vision Applications**: Apply deep learning techniques to image classification, object detection, and semantic segmentation tasks.

4. **Natural Language Processing**: Develop models for text classification, sentiment analysis, and sequence-to-sequence learning problems.

5. **Research Skills**: Critically evaluate current research literature and propose novel solutions to open problems in the field.

## Weekly Schedule

### Week 1-2: Foundations
- Introduction to Machine Learning Review
- Neural Network Basics and Perceptrons
- Backpropagation Algorithm
- **Lab**: Implementing a neural network from scratch

### Week 3-4: Deep Feedforward Networks
- Universal Approximation Theorem
- Activation Functions and Architecture Design
- Optimization Algorithms (SGD, Adam, etc.)
- **Assignment 1 Due**: Neural Network Fundamentals

### Week 5-7: Convolutional Neural Networks
- Convolution and Pooling Operations
- CNN Architectures (LeNet, AlexNet, VGG, ResNet)
- Transfer Learning and Fine-tuning
- **Lab**: Image Classification with CNNs

### Week 8: Midterm Examination
- Comprehensive exam covering weeks 1-7
- **Assignment 2 Due**: Convolutional Neural Networks

### Week 9-11: Recurrent Neural Networks
- RNN Fundamentals and Backpropagation Through Time
- Long Short-Term Memory (LSTM) Networks
- Gated Recurrent Units (GRUs)
- **Lab**: Sequence Modeling and Text Generation

### Week 12-13: Advanced Topics
- Attention Mechanisms and Transformers
- Generative Adversarial Networks (GANs)
- Reinforcement Learning with Deep Q-Networks
- **Assignment 3 Due**: Recurrent Neural Networks

### Week 14-15: Final Projects
- Project Presentations
- Current Research Trends Discussion
- Course Review and Future Directions

## Assessment Methods

### Homework Assignments (40%)
- **Assignment 1**: Neural Network Implementation (10%)
- **Assignment 2**: CNN for Computer Vision (15%)
- **Assignment 3**: RNN for Sequence Modeling (15%)

### Examinations (20%)
- **Midterm Exam**: Comprehensive assessment of theoretical concepts

### Final Project (30%)
- Team-based research project
- Options include:
  - Novel architecture design
  - Application to new domain
  - Comparative analysis study
  - Reproduction of recent research

### Class Participation (10%)
- Active participation in discussions
- Quality of questions and contributions
- Peer review of project proposals

## Required Resources

### Textbooks
1. **Primary**: "Deep Learning" by Goodfellow, Bengio, and Courville
2. **Supplementary**: "Pattern Recognition and Machine Learning" by Christopher Bishop

### Software and Tools
- **Programming Language**: Python 3.8 or higher
- **Deep Learning Frameworks**: TensorFlow 2.x and PyTorch
- **Development Environment**: Jupyter Notebooks, Google Colab
- **Version Control**: Git and GitHub for project management

### Hardware Requirements
- GPU access provided through university computing cluster
- Google Colab Pro recommended for intensive computations
- Minimum 8GB RAM for local development

## Course Policies

### Attendance Policy
Regular attendance is essential for success in this course. More than two unexcused absences may result in a reduction of the final grade.

### Late Submission Policy
- Assignments submitted late will incur a 10% penalty per day
- No assignments will be accepted more than 3 days past the due date
- Extensions may be granted for documented emergencies

### Academic Integrity
- Individual work is required for all assignments unless explicitly stated
- Collaboration on learning and discussion is encouraged
- Proper citation required for all external resources
- Violations will result in course failure

### Accessibility Services
Students requiring accommodations should contact the Office of Disability Services early in the semester to arrange appropriate support.

## Additional Information

### Office Hours
- **Instructor**: Wednesdays 2:00-4:00 PM, Klaus 2138
- **Teaching Assistants**: 
  - TA1: Mondays 1:00-3:00 PM, Klaus Graduate Lab
  - TA2: Fridays 10:00-12:00 PM, Klaus Graduate Lab

### Communication
- Course announcements via Canvas
- Discussion forum for technical questions
- Email for personal matters (response within 24 hours)

### Prerequisites Knowledge Check
Students should be comfortable with:
- Linear algebra (matrix operations, eigenvalues)
- Calculus (partial derivatives, chain rule)
- Probability and statistics
- Python programming
- Basic machine learning concepts

### Career Connections
This course prepares students for:
- Machine Learning Engineer positions
- Research roles in AI/ML
- PhD studies in Computer Science
- Data Science and Analytics careers
- Startup opportunities in AI domain

---

