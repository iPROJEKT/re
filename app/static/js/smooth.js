function scrollToEvents(eventId) {
    document.getElementById('standard-events').style.display = 'none';
    document.getElementById('nonstandard-events').style.display = 'none';
    document.getElementById(eventId).style.display = 'block';
    document.getElementById('events-section').scrollIntoView({ behavior: 'smooth' });
}