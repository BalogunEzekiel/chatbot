import time
import sys
import platform

# For Windows: use winsound to play a beep
if platform.system() == "Windows":
    import winsound

# Simulate typing with sound (Windows only)
def type_with_sound(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)  # Slower typing simulation
        if platform.system() == "Windows":
            winsound.Beep(1000, 30)  # frequency, duration in ms
    print()  # for new line

# Response generator
def get_livestock_response(user_input):
    user_input_lower = user_input.lower()
    if "hi" in user_input_lower or "hello" in user_input_lower:
        return "Hello there! How can I help you today?"

    elif "help" in user_input_lower:
        return "Sure, I’m here to help! Can you tell me a bit more about what you need?"
    elif "assist" in user_input_lower:
        return "Absolutely! Just let me know what you're looking for or need help with about animal care."
    elif "new" in user_input_lower:
        return "Welcome! 🎉 I'm glad you're here. Would you like a quick tour of VetSmart app or ask me questions about livestock."
    elif "yes" in user_input_lower or "alright" in user_input_lower:
        return "That's okay!."
    elif "thanks" in user_input_lower or "thank you" in user_input_lower:
        return "You're welcome!."
    elif "bye" in user_input_lower or "goodbye" in user_input_lower:
        return "Goodbye!."
    elif "no" in user_input_lower or "ok" in user_input_lower or "okay" in user_input_lower:
        return "Alrigt."
    elif "exercise" in user_input_lower:
        return "Regular movement is beneficial; ensure adequate pasture space."
    elif "social" in user_input_lower:
        return "Yes, animals thrive in groups."
    elif "biosecurity" in user_input_lower:
        return "Limit outside animal contact, quarantine new animals, and sanitize equipment."
    elif "zoonotic" in user_input_lower:
        return "Yes, such as brucellosis and Q fever; practice good hygiene."
    elif "foot rot" in user_input_lower:
        return "A bacterial infection causing lameness; prevent with dry conditions and hoof care."
    elif "internal parasite" in user_input_lower:
        return "Regular deworming and rotational grazing."
    elif "common diseases" in user_input_lower:
        return "Respiratory infections, parasitic infestations, and foot rot."
    elif "ventilation" in user_input_lower:
        return "Yes, proper ventilation reduces respiratory issues."
    elif "bedding" in user_input_lower:
        return "Regularly, at least once a week, to maintain cleanliness."
    elif "floor" in user_input_lower:
        return "Non-slip, easy-to-clean surfaces like packed dirt or rubber mats."
    elif "space" in user_input_lower:
        return "Cattle: ~20-50 sq. ft. indoors; Goats/Sheep: ~15-20 sq. ft."
    elif "shelter" in user_input_lower:
        return "Protection from extreme weather; well-ventilated barns or sheds."
    elif "breeding" in user_input_lower:
        return "Cattle: ~12 months; Goats/Sheep: 7-9 months."
    elif "offspring" in user_input_lower:
        return "Cattle: usually one; Goats/Sheep: one to three."
    elif "heat" in user_input_lower:
        return "Restlessness, vocalization and mounting behavior."
    elif "gestation" in user_input_lower:
        return "Cattle: ~283 days; Goats: ~150 days; Sheep: ~147 days."
    elif "toxic" in user_input_lower:
        return "Yes, plants like oleander, rhododendron and certain types of nightshade are toxic."
    elif "water" in user_input_lower:
        return "Cattle: 10-20 gallons; Goats/Sheep: 1-4 gallons, depending on size and climate."
    elif "grazing together" in user_input_lower:
        return "Yes, but monitor to prevent overgrazing and ensure balanced nutrition."
    elif "diet" in user_input_lower:
        return "Primarily forage-based, supplemented with grains as needed."
    elif "mature" in user_input_lower:
        return "Cattle: 1-2 years; Goats: 6-12 months; Sheep: 6-12 months."
    elif "live" in user_input_lower:
        return "Cattle can live up to 20 years, while goats and sheep often live around 10 to 12 years, depending on breed and care."
    elif "fever" in user_input_lower:
        return "A fever in livestock can indicate an infection. Isolate the animal and consult a veterinarian."
    elif "diarrhea" in user_input_lower:
        return "Diarrhea may result from parasites or poor diet. Keep the animal hydrated and call a vet."
    elif "not eating" in user_input_lower or "loss of appetite" in user_input_lower:
        return "A loss of appetite could mean illness. Watch for other signs and contact an expert."
    elif "vaccination" in user_input_lower:
        return "Vaccinations are essential. Ask a vet for a schedule tailored to your animals."
    elif "bloat" in user_input_lower:
        return "Bloat is serious and life-threatening. Avoid risky feed and act fast — call your vet."
    else:
        return "Can you provide more information about your livestock’s symptoms or behavior?"

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break
        response = get_livestock_response(user_input)
        type_with_sound("VetSmart: " + response)
