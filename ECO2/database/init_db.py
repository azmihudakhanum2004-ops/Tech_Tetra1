#!/usr/bin/env python3
"""
Database initialization script for EcoLearn.
Run this script to set up the database with sample data.
"""

from app import app, db, User, Lesson, Quiz, Challenge, Badge
import json

def init_sample_data():
    """Initialize the database with sample data."""

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if data already exists
        if Lesson.query.count() > 0:
            print("Sample data already exists. Skipping initialization.")
            return

        print("Initializing sample data...")

        # Sample lessons
        lessons_data = [
            {
                'title': 'Introduction to Climate Change',
                'description': 'Learn the basics of climate change and its impacts on our planet',
                'content': '''
                <h2>What is Climate Change?</h2>
                <p>Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas.</p>

                <h2>Key Impacts</h2>
                <ul>
                    <li>Rising sea levels</li>
                    <li>More frequent and intense extreme weather events</li>
                    <li>Changes in ecosystems and biodiversity</li>
                    <li>Impacts on agriculture and food security</li>
                </ul>

                <h2>What Can We Do?</h2>
                <p>Individual actions matter! Reducing energy consumption, using renewable energy, and supporting sustainable practices can help mitigate climate change.</p>
                ''',
                'category': 'climate',
                'difficulty': 'beginner',
                'points_reward': 20
            },
            {
                'title': 'Waste Management Solutions',
                'description': 'Discover effective ways to manage and reduce waste in our daily lives',
                'content': '''
                <h2>The Waste Problem</h2>
                <p>Every year, humans generate billions of tons of waste. Much of this waste ends up in landfills or oceans, causing environmental pollution and harming wildlife.</p>

                <h2>Reduce, Reuse, Recycle</h2>
                <ul>
                    <li><strong>Reduce:</strong> Buy products with less packaging, avoid single-use items</li>
                    <li><strong>Reuse:</strong> Use reusable bags, bottles, and containers</li>
                    <li><strong>Recycle:</strong> Sort waste properly and recycle materials like paper, plastic, and glass</li>
                </ul>

                <h2>Composting</h2>
                <p>Composting food scraps and yard waste creates nutrient-rich soil that can be used in gardens, reducing the need for chemical fertilizers.</p>
                ''',
                'category': 'waste',
                'difficulty': 'beginner',
                'points_reward': 25
            },
            {
                'title': 'Biodiversity Conservation',
                'description': 'Understand the importance of biodiversity and how to protect it',
                'content': '''
                <h2>What is Biodiversity?</h2>
                <p>Biodiversity refers to the variety of life on Earth, including plants, animals, microorganisms, and the ecosystems they form. It's essential for maintaining healthy ecosystems.</p>

                <h2>Why Biodiversity Matters</h2>
                <ul>
                    <li>Provides food, medicine, and materials</li>
                    <li>Regulates climate and water cycles</li>
                    <li>Supports pollination and soil fertility</li>
                    <li>Offers recreational and cultural benefits</li>
                </ul>

                <h2>Conservation Actions</h2>
                <p>Create wildlife habitats in your backyard, support conservation organizations, reduce pesticide use, and choose sustainable products.</p>
                ''',
                'category': 'biodiversity',
                'difficulty': 'intermediate',
                'points_reward': 30
            }
        ]

        # Add lessons and their quizzes
        for lesson_data in lessons_data:
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
            db.session.flush()  # Get the lesson ID

            # Add quiz questions for each lesson
            if lesson.title == 'Introduction to Climate Change':
                quizzes = [
                    {
                        'question': 'What is the primary driver of climate change since the 1800s?',
                        'options': json.dumps(['Natural processes', 'Burning fossil fuels', 'Solar activity', 'Volcanic eruptions']),
                        'correct_answer': 1,
                        'explanation': 'Human activities, primarily burning fossil fuels, have been the main driver of climate change since the 1800s.'
                    },
                    {
                        'question': 'Which of these is NOT a key impact of climate change?',
                        'options': json.dumps(['Rising sea levels', 'More frequent extreme weather', 'Increased biodiversity', 'Changes in agriculture']),
                        'correct_answer': 2,
                        'explanation': 'Climate change typically reduces biodiversity, not increases it.'
                    }
                ]
            elif lesson.title == 'Waste Management Solutions':
                quizzes = [
                    {
                        'question': 'What does the "Three Rs" stand for in waste management?',
                        'options': json.dumps(['Reduce, Reuse, Recycle', 'Repair, Reuse, Recycle', 'Reduce, Repair, Recycle', 'Reuse, Recycle, Recover']),
                        'correct_answer': 0,
                        'explanation': 'The Three Rs are Reduce, Reuse, and Recycle - the foundation of waste management.'
                    },
                    {
                        'question': 'What type of waste is best for composting?',
                        'options': json.dumps(['Plastic bottles', 'Food scraps and yard waste', 'Electronic waste', 'Glass jars']),
                        'correct_answer': 1,
                        'explanation': 'Food scraps and yard waste are organic materials that break down naturally in compost.'
                    }
                ]
            else:  # Biodiversity Conservation
                quizzes = [
                    {
                        'question': 'What is biodiversity?',
                        'options': json.dumps(['Number of species in an area', 'Variety of life on Earth', 'Size of ecosystems', 'Amount of pollution']),
                        'correct_answer': 1,
                        'explanation': 'Biodiversity refers to the variety of life on Earth, including all living organisms and ecosystems.'
                    },
                    {
                        'question': 'Which of these is NOT a benefit of biodiversity?',
                        'options': json.dumps(['Provides food and medicine', 'Regulates climate', 'Increases pollution', 'Supports soil fertility']),
                        'correct_answer': 2,
                        'explanation': 'Biodiversity helps reduce pollution and supports healthy ecosystems, not increases pollution.'
                    }
                ]

            for quiz_data in quizzes:
                quiz = Quiz(lesson_id=lesson.id, **quiz_data)
                db.session.add(quiz)

        # Sample challenges
        challenges_data = [
            {
                'title': 'Plant a Tree',
                'description': 'Plant a tree in your neighborhood, school, or community garden. Document your planting with photos and share what species you planted.',
                'category': 'conservation',
                'points_reward': 100,
                'duration_days': 30
            },
            {
                'title': 'Plastic-Free Week',
                'description': 'Avoid using single-use plastics for one week. Use reusable bags, bottles, and containers instead.',
                'category': 'waste',
                'points_reward': 75,
                'duration_days': 7
            },
            {
                'title': 'Water Conservation Challenge',
                'description': 'Implement water-saving practices for two weeks. Fix leaks, take shorter showers, and use water-efficient appliances.',
                'category': 'conservation',
                'points_reward': 80,
                'duration_days': 14
            },
            {
                'title': 'Bicycle Commute',
                'description': 'Replace car trips with bicycle rides for a week. Track your carbon savings and share your experience.',
                'category': 'transportation',
                'points_reward': 90,
                'duration_days': 7
            }
        ]

        for challenge_data in challenges_data:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)

        # Sample badges
        badges_data = [
            {
                'name': 'Eco Warrior',
                'description': 'Complete 5 environmental challenges',
                'criteria': 'challenges_completed:5'
            },
            {
                'name': 'Climate Scholar',
                'description': 'Complete all climate change lessons',
                'criteria': 'lessons_completed:climate'
            },
            {
                'name': 'Point Master',
                'description': 'Earn 500 eco-points',
                'criteria': 'points_threshold:500'
            },
            {
                'name': 'Waste Warrior',
                'description': 'Complete all waste management lessons',
                'criteria': 'lessons_completed:waste'
            },
            {
                'name': 'Conservation Champion',
                'description': 'Complete 10 environmental challenges',
                'criteria': 'challenges_completed:10'
            }
        ]

        for badge_data in badges_data:
            badge = Badge(**badge_data)
            db.session.add(badge)

        # Commit all changes
        db.session.commit()

        print("Sample data initialized successfully!")
        print(f"Added {len(lessons_data)} lessons, {len(challenges_data)} challenges, and {len(badges_data)} badges.")

if __name__ == '__main__':
    init_sample_data()
