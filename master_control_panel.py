"""
Bitcoin ECDLP - Master Control Panel
Integrated menu for all simulators and analysis tools
"""

import os
import sys
import subprocess

def print_header():
    """Print main header"""
    print("\n" * 2)
    print("="*90)
    print(" "*20 + "🪙 BITCOIN ECDLP - MASTER CONTROL PANEL 🪙")
    print("="*90)
    print()

def print_main_menu():
    """Print main menu"""
    print("┌" + "─"*88 + "┐")
    print("│" + " "*88 + "│")
    print("│  📊 MAIN MODULES                                                                    │")
    print("│" + " "*88 + "│")
    print("│  1. 🎮 Interactive Attack Simulator                                                 │")
    print("│     Test Brute Force, Pollard's Rho, Baby-Step Giant-Step on small curves          │")
    print("│                                                                                      │")
    print("│  2. 📈 Advanced Analysis & Visualization                                            │")
    print("│     Complexity plots, CSV export, Bitcoin comparison, Quantum analysis              │")
    print("│                                                                                      │")
    print("│  3. 🖥️  Distributed Attack Simulator                                                │")
    print("│     Simulate 10, 100, or 1000 GPU clusters attacking the puzzle                     │")
    print("│                                                                                      │")
    print("│  4. 📚 Educational Examples                                                         │")
    print("│     Manual ECDLP walkthrough and test suite                                         │")
    print("│                                                                                      │")
    print("│" + " "*88 + "│")
    print("│  🔧 UTILITIES                                                                       │")
    print("│" + " "*88 + "│")
    print("│  5. 📖 Documentation & Help                                                         │")
    print("│  6. ⚙️  System Information                                                          │")
    print("│  7. 📋 All Files Overview                                                           │")
    print("│  8. ❌ Exit                                                                         │")
    print("│" + " "*88 + "│")
    print("└" + "─"*88 + "┘")
    print()

def run_module(filename, description):
    """Run a Python module"""
    print()
    print("="*90)
    print(f"▶️  Running: {description}")
    print("="*90)
    print()
    
    try:
        subprocess.run([sys.executable, filename], check=False)
    except FileNotFoundError:
        print(f"❌ ERROR: File '{filename}' not found!")
        print(f"   Make sure you're in the correct directory: {os.getcwd()}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    input("Press Enter to return to main menu...")

def print_documentation():
    """Print help and documentation"""
    print()
    print("="*90)
    print("📖 BITCOIN ECDLP TOOLKIT - DOCUMENTATION")
    print("="*90)
    print()
    
    docs = """
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                            QUICK START GUIDE                                              │
└────────────────────────────────────────────────────────────────────────────────────────────┘

1️⃣  BEGINNERS: Start with Educational Examples
    ↓
    Run: example_manual_ecdlp.py
    Learn: How ECDLP works on tiny curves with manual calculation
    Time: ~2 minutes
    
2️⃣  INTERMEDIATE: Try Attack Simulator
    ↓
    Run: interactive_attack_simulator.py
    Learn: Compare Brute Force, Pollard's Rho, Baby-Step Giant-Step
    Time: ~5-10 minutes
    
3️⃣  ADVANCED: Run All Simulators
    ↓
    Run: This menu system
    Learn: Everything - complexity, distributions, quantum threats
    Time: Unlimited exploration

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                           ALGORITHM COMPLEXITY                                            │
└────────────────────────────────────────────────────────────────────────────────────────────┘

Algorithm               | Time Complexity | Space | Best For              | Notes
─────────────────────────────────────────────────────────────────────────────────────────────
Brute Force            | O(N)           | O(1)  | Small curves          | Simple, no storage
Pollard's Rho          | O(√N)          | O(1)  | Large search space    | Cycle detection
Baby-Step Giant-Step   | O(√N)          | O(√N) | Medium curves         | Memory tradeoff
Kangaroo Algorithm     | O(√N)          | O(1)  | Range queries         | Best for Puzzle#71
Quantum (Grover)       | O(∛N)          | ?     | Post-quantum era      | If quantum ready

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                        BITCOIN PUZZLE STATISTICS                                          │
└────────────────────────────────────────────────────────────────────────────────────────────┘

Puzzle #71 Parameters:
  • Target address: 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU
  • Reward: 7.10154982 BTC (~$300,000+)
  • Search space: 2^270 to 2^271 (~3.7 × 10^81 keys)
  • Status: UNSOLVED (since 2019)
  • Estimated effort: 1-5 years with 1000 GPUs
  • Cost: $3-5 million for continuous operation

Attack Time Estimates (Average Case):
  • 1 GPU:      10^30 years (IMPOSSIBLE)
  • 100 GPUs:   10^28 years (IMPOSSIBLE)
  • 1,000 GPUs: 1-5 years (FEASIBLE but expensive)
  • 10,000 GPUs: ~1-2 months (VERY expensive)

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                          FILE DESCRIPTIONS                                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘

Core Modules:
  test_bitcoin_puzzle.py              8 comprehensive tests for secp256k1
  example_manual_ecdlp.py             Manual walkthrough with small numbers
  interactive_attack_simulator.py     Compare attacks interactively
  advanced_analysis.py                Complexity plots, CSV export, comparisons
  distributed_attack_simulator.py     Multi-GPU cluster simulation

Supporting Files:
  requirements.txt                    Python dependencies
  Dockerfile                          Docker container
  docker-compose.yml                  Multi-service orchestration
  Dockerfile.cuda                     CUDA-enabled GPU container
  run_tests.sh                         Automated test runner
  README_TESTING.md                   Complete testing guide
  .github/workflows/test.yml          GitHub Actions CI/CD

Original Files (Project Root):
  Bitcoin_Puzzle_71_Colab.ipynb       Google Colab notebook
  Bitcoin_Puzzle_71_Colab_Fixed.ipynb Enhanced Colab version
  pollard_rho_cuda.py                 CPU + CUDA Pollard's Rho
  pollard_rho_gpu_cuda.py             Full GPU Pollard's Rho
  Nexusse                             Solidity BEP20 token contract

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                           KEYBOARD SHORTCUTS                                              │
└────────────────────────────────────────────────────────────────────────────────────────────┘

During any simulator:
  • Press Ctrl+C to interrupt and return to menu
  • Press Enter to continue between screens
  • Type number and press Enter for menu choices

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                           FREQUENTLY ASKED QUESTIONS                                      │
└────────────────────────────────────────────────────────────────────────────────────────────┘

Q: Why are the curves so small?
A: We use P=17 for educational purposes. Real Bitcoin uses 2^256 (77 digits). The math is
   identical, but we can compute on small curves in milliseconds vs years for real Bitcoin.

Q: Will quantum computers break Bitcoin?
A: Grover's algorithm reduces effort from 2^256 to 2^128 operations. Bitcoin can upgrade to
   larger keys. ECDLP is still hard even for quantum computers (Shor's doesn't directly apply).

Q: When will Puzzle #71 be solved?
A: Current estimate: 1-5 years with 1000 GPUs or 1-3 months with 10,000+ GPUs. The effort
   required makes it economically marginal vs the reward.

Q: Why not use Pollard's Rho for real Bitcoin?
A: We do! But even O(√N) with N=2^256 means ~2^128 operations. That's still ~10^38 operations,
   which takes millennia on current hardware.

Q: Can this code break Bitcoin?
A: No. This is educational code on toy curves. The math for real Bitcoin (secp256k1) is
   identical, but the numbers are so large that it's computationally infeasible.

Q: How much would it cost to break Puzzle #71?
A: With current GPU prices (~$300 per V100):
   • 1,000 GPUs: $300,000 + $1M/year operating costs
   • Attempt duration: 1-5 years
   • Total: $1-5 million with uncertain success

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                           LEARNING RESOURCES                                              │
└────────────────────────────────────────────────────────────────────────────────────────────┘

Recommended Learning Path:

1. Read this documentation (5 min)
   ↓
2. Run example_manual_ecdlp.py (5 min)
   See: How point multiplication works on P=17
   ↓
3. Run test_bitcoin_puzzle.py (5 min)
   See: All 8 tests pass, verify implementation
   ↓
4. Run interactive_attack_simulator.py (10-30 min)
   Try: All attack types, race simulation
   ↓
5. Run advanced_analysis.py (30 min)
   Explore: Complexity analysis, Bitcoin comparison
   ↓
6. Run distributed_attack_simulator.py (30 min)
   Simulate: 10, 100, 1000 GPU clusters
   ↓
7. Read source code and modify scenarios

───────────────────────────────────────────────────────────────────────────────────────────────

For more information, visit:
  • Bitcoin Wiki: https://en.bitcoin.it/wiki/Secp256k1
  • ECDLP: https://en.wikipedia.org/wiki/Elliptic_curve_discrete_logarithm_problem
  • Pollard's Rho: https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm_for_logarithms
  • Bitcoin Puzzle: https://github.com/bitcoin-core/bitcoin-core.github.io/issues/

──────────────────────────────────────────────────────────────────────────────���────────────────
    """
    print(docs)

def print_system_info():
    """Print system information"""
    print()
    print("="*90)
    print("⚙️  SYSTEM INFORMATION")
    print("="*90)
    print()
    
    import platform
    import math
    
    print(f"Python Version:    {sys.version.split()[0]}")
    print(f"Platform:          {platform.system()} {platform.release()}")
    print(f"Architecture:      {platform.architecture()[0]}")
    print(f"Current Directory: {os.getcwd()}")
    print()
    
    # Check installed packages
    packages = {
        'numpy': '📦 NumPy',
        'matplotlib': '📊 Matplotlib',
        'numba': '⚡ Numba',
        'requests': '🌐 Requests',
        'pandas': '📋 Pandas'
    }
    
    print("Installed Packages:")
    print("-"*90)
    
    for package, label in packages.items():
        try:
            __import__(package)
            print(f"✅ {label:<20} - Available")
        except ImportError:
            print(f"❌ {label:<20} - Not installed (optional)")
    
    print()
    print("Installation hints:")
    print("  pip install -r requirements.txt")
    print()

def print_files_overview():
    """Print overview of all project files"""
    print()
    print("="*90)
    print("📋 PROJECT FILES OVERVIEW")
    print("="*90)
    print()
    
    files_info = {
        'Core Educational': [
            ('example_manual_ecdlp.py', 'Manual ECDLP walkthrough (P=17)'),
            ('test_bitcoin_puzzle.py', '8 comprehensive tests'),
        ],
        'Interactive Simulators': [
            ('interactive_attack_simulator.py', 'Compare 3 attack algorithms'),
            ('advanced_analysis.py', 'Complexity analysis & visualization'),
            ('distributed_attack_simulator.py', 'Multi-GPU cluster simulation'),
        ],
        'GPU/CUDA Original': [
            ('Bitcoin_Puzzle_71_Colab.ipynb', 'Google Colab notebook'),
            ('pollard_rho_cuda.py', 'CPU + CUDA Pollard\'s Rho'),
            ('pollard_rho_gpu_cuda.py', 'Full GPU Pollard\'s Rho'),
        ],
        'Infrastructure': [
            ('requirements.txt', 'Python dependencies'),
            ('Dockerfile', 'Docker container'),
            ('docker-compose.yml', 'Multi-service orchestration'),
            ('Dockerfile.cuda', 'CUDA-enabled container'),
            ('.github/workflows/test.yml', 'GitHub Actions CI/CD'),
            ('run_tests.sh', 'Automated test runner'),
        ],
        'Documentation': [
            ('README_TESTING.md', 'Complete testing guide'),
            ('this_file', 'Master control panel'),
        ]
    }
    
    for category, items in files_info.items():
        print(f"\n{category}:")
        print("-" * 90)
        for filename, description in items:
            status = "✅" if filename == 'this_file' or os.path.exists(filename) else "📄"
            print(f"  {status} {filename:<30} - {description}")
    
    print()

def main():
    """Main control panel loop"""
    print_header()
    
    modules = {
        '1': {
            'name': 'Interactive Attack Simulator',
            'file': 'interactive_attack_simulator.py',
            'desc': 'Test Brute Force, Pollard\'s Rho, Baby-Step Giant-Step'
        },
        '2': {
            'name': 'Advanced Analysis & Visualization',
            'file': 'advanced_analysis.py',
            'desc': 'Complexity plots, Bitcoin comparison, Quantum analysis'
        },
        '3': {
            'name': 'Distributed Attack Simulator',
            'file': 'distributed_attack_simulator.py',
            'desc': 'Simulate 10, 100, 1000 GPU clusters'
        },
        '4': {
            'name': 'Educational Examples',
            'file': 'example_manual_ecdlp.py',
            'desc': 'Manual ECDLP walkthrough on tiny curves'
        }
    }
    
    while True:
        print_main_menu()
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice in modules:
            module = modules[choice]
            run_module(module['file'], module['desc'])
        
        elif choice == '5':
            print_documentation()
            input("\nPress Enter to return to main menu...")
        
        elif choice == '6':
            print_system_info()
            input("Press Enter to return to main menu...")
        
        elif choice == '7':
            print_files_overview()
            input("Press Enter to return to main menu...")
        
        elif choice == '8':
            print()
            print("="*90)
            print("👋 Thank you for using Bitcoin ECDLP Toolkit!")
            print("="*90)
            print()
            print("Summary of what you learned:")
            print("  ✅ ECDLP fundamentals on small curves")
            print("  ✅ Attack algorithms: Brute Force, Pollard's Rho, Baby-Step Giant-Step")
            print("  ✅ Why Bitcoin is secure (secp256k1 has huge key space)")
            print("  ✅ Distributed computing challenges")
            print("  ✅ Quantum computing implications")
            print()
            print("Further reading:")
            print("  📖 Bitcoin Wiki: https://en.bitcoin.it")
            print("  🔗 ECDLP: https://en.wikipedia.org/wiki/Elliptic_curve_discrete_logarithm_problem")
            print()
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("👋 Interrupted. Goodbye!")
        sys.exit(0)
