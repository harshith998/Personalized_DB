from pipeline import process_email

def main():
    print("🤖 3-LLM Email Response System")
    print("="*70)
    print("Available test users:")
    print("  - john.doe@company.com (Senior Engineer, standard clearance)")
    print("  - intern@company.com (Intern, limited clearance)")
    print("  - cfo@company.com (CFO, executive clearance)")
    print("\\nAvailable documents:")
    print("  - Q4 2024 Financial Report (executive only)")
    print("  - API Documentation v2.1 (standard clearance)")
    print("  - New Hire Onboarding Guide (limited clearance)")
    print("  - Engineering Playbook (standard clearance)")
    print("="*70)
    print()
    
    while True:
        print("\\n" + "="*70)
        sender = input("From (email address): ").strip()
        
        if not sender:
            print("👋 Exiting...")
            break
        
        subject = input("Subject: ").strip()
        if not subject:
            subject = "Document Request"
        
        print("Body (press Enter twice to finish):")
        body_lines = []
        while True:
            line = input()
            if line == "":
                if body_lines and body_lines[-1] == "":
                    body_lines.pop()
                    break
            body_lines.append(line)
        
        body = "\\n".join(body_lines)
        
        if not body:
            print("❌ Email body cannot be empty")
            continue
        
        # Process the email through pipeline
        process_email(sender, subject, body)

if __name__ == "__main__":
    main()