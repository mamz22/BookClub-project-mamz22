from queries import (
    get_all_books_with_avg_rating,
    get_users_in_club,
    get_comments_for_book,
    get_discussion_comments,
    get_top_3_active_clubs,
    get_top_rated_books,
    add_user,
    add_book,
    join_club,
    post_book_comment,
    rate_book,
    start_discussion,
    comment_on_discussion,
    find_user_id,
    find_book_id
)

def main():
    while True:
        print("--- Book Club App Menu ---")
        print("1. View all books with average ratings")
        print("2. View users in a book club")
        print("3. View comments for a book")
        print("4. View discussions and comments in a club")
        print("5. View top 3 most active clubs")
        print("6. View top-rated books (rating ≥ 4)")
        print("7. Register a new user")
        print("8. Add a new book")
        print("9. Join a book club")
        print("10. Post a book comment")
        print("11. Rate a book")
        print("12. Start a discussion")
        print("13. Comment on a discussion")
        print("14. Find your User ID by username")
        print("15. Find your Book ID by book name")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            get_all_books_with_avg_rating()
        elif choice == '2':
            club_id = input("Enter Club ID: ")
            get_users_in_club(int(club_id))
        elif choice == '3':
            book_id = input("Enter Book ID: ")
            get_comments_for_book(int(book_id))
        elif choice == '4':
            club_id = input("Enter Club ID: ")
            get_discussion_comments(int(club_id))
        elif choice == '5':
            get_top_3_active_clubs()
        elif choice == '6':
            get_top_rated_books()
        elif choice == '7':
            add_user()
        elif choice == '8':
            add_book()
        elif choice == '9':
            join_club()
        elif choice == '10':
            post_book_comment()
        elif choice == '11':
            rate_book()
        elif choice == '12':
            start_discussion()
        elif choice == '13':
            comment_on_discussion()
        elif choice == '14':
            find_user_id()
        elif choice == '15':
            find_book_id()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
