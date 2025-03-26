import React, { useState } from 'react';

function ComplexComponent() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <h1>Accessibility Test Page</h1>

      {/* Missing proper heading structure */}
      <div className="section-title">Main Section</div>

      {/* Non-semantic clickable div */}
      <div onClick={() => alert('Clicked!')} style={{ cursor: 'pointer' }}>
        Click Me!
      </div>

      {/* Image without alt text */}
      <img src="https://example.com/image.jpg" />

      {/* Form with missing labels */}
      <form>
        <input type="text" placeholder="Enter your name" />
        <button>Submit</button>
      </form>

      {/* Modal without focus management */}
      <button onClick={() => setIsOpen(true)}>Open Modal</button>
      {isOpen && (
        <div className="modal" role="dialog">
          <div>
            <h2>Modal Title</h2>
            <p>This is a modal with no focus management.</p>
            <button onClick={() => setIsOpen(false)}>Close Modal</button>
          </div>
        </div>
      )}

      {/* Poor color contrast */}
      <p style={{ color: '#ccc', backgroundColor: '#fff' }}>
        This text has poor color contrast.
      </p>

      {/* Link without descriptive text */}
      <a href="https://example.com">Click here</a>

      {/* Keyboard navigation issue */}
      <div tabIndex="0">This div is unnecessarily focusable.</div>

      {/* Missing ARIA roles on a custom dropdown */}
      <div className="dropdown">
        <div className="dropdown-header" onClick={() => console.log('Open dropdown')}>
          Select an option
        </div>
        <ul className="dropdown-menu">
          <li>Option 1</li>
          <li>Option 2</li>
          <li>Option 3</li>
        </ul>
      </div>

      {/* Video without captions */}
      <video controls>
        <source src="example.mp4" type="video/mp4" />
      </video>
    </div>
  );
}

export default ComplexComponent;
