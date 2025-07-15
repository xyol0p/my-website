#!/bin/bash

# Automatic Report System - ZIP Creator
echo "📦 Creating ZIP package for Automatic Report System..."

# ZIP file name with timestamp
ZIP_NAME="automatic_report_system_$(date +%Y%m%d_%H%M%S).zip"

echo "🗂️  Packaging files..."

# Create ZIP file with all important files
zip -r "$ZIP_NAME" \
    main.py \
    config.py \
    data_collector.py \
    report_generator.py \
    scheduler.py \
    requirements.txt \
    README.md \
    SYSTEM_OVERVIEW.md \
    quick_start.sh \
    create_zip.sh \
    reports/ \
    data/ \
    templates/ \
    logs/ \
    -x "venv/*" "__pycache__/*" "*.pyc" ".git/*"

echo "✅ ZIP file created: $ZIP_NAME"
echo "📊 File size: $(du -h "$ZIP_NAME" | cut -f1)"
echo ""
echo "📋 Contents included:"
echo "   ✓ All Python source files"
echo "   ✓ Configuration files"
echo "   ✓ Generated reports"
echo "   ✓ Documentation"
echo "   ✓ Quick start script"
echo "   ✓ Sample data"
echo ""
echo "🚀 To use on another system:"
echo "   1. Extract: unzip $ZIP_NAME"
echo "   2. Setup: ./quick_start.sh"
echo "   3. Test: ./quick_start.sh sample"
echo ""
echo "🎉 Your complete Automatic Report System is ready!"