import curses
import random
import time

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green text
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Red text
    
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    
    hex_digits = "0123456789ABCDEF"
    
    # Display 16 screens
    for screen in range(16):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Generate and display random hex digits
        for row in range(height):
            # Build a string of random hex digits for the entire row
            hex_row = ''.join(random.choice(hex_digits) for _ in range(width))
            try:
                if row < height - 1:
                    stdscr.addstr(row, 0, hex_row, curses.color_pair(1))
                else:
                    # Handle last row carefully
                    if width > 0:
                        if width > 1:
                            stdscr.addstr(row, 0, hex_row[:-1], curses.color_pair(1))
                        stdscr.addch(row, width-1, hex_row[-1], curses.color_pair(1))
            except curses.error:
                pass
        
        stdscr.refresh()
        
        # Wait 1.5 seconds or until 'q' pressed
        start_time = time.time()
        while time.time() - start_time < 1.5:
            if stdscr.getch() in (ord('q'), ord('Q')):  # Fixed syntax
                return
            time.sleep(0.05)
    
    # Main loop for replacing random numerals
    while True:
        height, width = stdscr.getmaxyx()
        if height < 1 or width < 1:
            continue
            
        # Select random position (avoid bottom-right corner to prevent scrolling)
        row = random.randint(0, height - 1)
        col = random.randint(0, width - 1)
        if row == height - 1 and col == width - 1:
            continue  # Skip bottom-right corner
        
        # Get original character
        try:
            original_char = stdscr.inch(row, col) & 0xFF
            original_char = chr(original_char)
        except curses.error:
            continue
        
        # Skip if not a hex digit
        if original_char not in hex_digits:
            continue
        
        # Replace with random red numeral
        new_red_digit = random.choice(hex_digits)
        try:
            stdscr.addch(row, col, new_red_digit, curses.color_pair(2))
            stdscr.refresh()
        except curses.error:
            pass
        
        # Wait 1.5 seconds or until 'q' pressed
        start_time = time.time()
        while time.time() - start_time < 1.5:
            if stdscr.getch() in (ord('q'), ord('Q')):  # Fixed syntax
                return
            time.sleep(0.05)
        
        # Change back to green
        try:
            stdscr.addch(row, col, new_red_digit, curses.color_pair(1))
            stdscr.refresh()
        except curses.error:
            pass

if __name__ == "__main__":
    curses.wrapper(main)
