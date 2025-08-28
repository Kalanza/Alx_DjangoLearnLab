// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
    
    // Add smooth scrolling to navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add a subtle animation effect when clicking nav links
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Add hover effects to posts
    const posts = document.querySelectorAll('.post');
    posts.forEach(post => {
        post.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 4px 10px rgba(0,0,0,0.2)';
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        post.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
            this.style.transform = 'translateY(0)';
        });
    });
});
