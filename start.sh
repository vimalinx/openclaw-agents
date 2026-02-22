#!/bin/bash

# Algora Bounty Tools - Quick Start Script
# Run this to explore all the tools!

echo "🎯 Algora Bounty Tools - Quick Start"
echo "=================================="
echo ""

# Check if SDK is installed
if [ ! -d "node_modules/@algora" ]; then
    echo "📦 Installing Algora SDK..."
    npm install @algora/sdk
    echo ""
fi

echo "What would you like to do?"
echo ""
echo "1. 🔍 Explore top bounties (recommended first)"
echo "2. 🔎 Search for specific bounties"
echo "3. 📋 View all bounties for Cal.com"
echo "4. 🎨 Generate interactive dashboard"
echo "5. 💻 Launch interactive CLI"
echo "6. 📊 Run full exploration (all organizations)"
echo ""
echo "Enter your choice (1-6):"
read choice

case $choice in
    1)
        echo ""
        echo "🏆 Showing top 15 bounties..."
        echo ""
        node top-bounties-fixed.mjs 15
        ;;
    2)
        echo ""
        echo "Enter a keyword to search for:"
        read keyword
        echo "Enter minimum reward (press enter for no minimum):"
        read reward
        echo ""
        if [ -z "$reward" ]; then
            node search-bounties.mjs "$keyword"
        else
            node search-bounties.mjs "$keyword" "$reward"
        fi
        ;;
    3)
        echo ""
        echo "📋 Viewing Cal.com bounties..."
        echo ""
        node bounty-viewer.mjs
        ;;
    4)
        echo ""
        echo "🎨 Generating dashboard..."
        node generate-dashboard.mjs
        echo ""
        echo "✅ Dashboard generated: bounty-dashboard.html"
        echo "💡 Opening in browser..."
        if command -v xdg-open > /dev/null; then
            xdg-open bounty-dashboard.html
        elif command -v open > /dev/null; then
            open bounty-dashboard.html
        else
            echo "Please open bounty-dashboard.html in your browser manually"
        fi
        ;;
    5)
        echo ""
        echo "💻 Launching interactive CLI..."
        echo ""
        node bounty-cli.mjs
        ;;
    6)
        echo ""
        echo "📊 Running full exploration (this may take a moment)..."
        echo ""
        node algora-full-explorer.mjs
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "✅ Done!"
echo ""
echo "📚 Documentation:"
echo "   - ALGORA_TOOLS_README.md - Quick reference for all tools"
echo "   - ALGORA_EXPLORATION_REPORT.md - Comprehensive report"
echo "   - EXPLORATION_SUMMARY.md - This exploration summary"
echo ""
echo "🔗 Links:"
echo "   - Algora: https://algora.io"
echo "   - Docs: https://algora.io/docs"
echo ""
