import configparser
import random

from loguru import logger

from parser_sentences import get_sentences


class Bot:

    def __init__(self, config_path: str) -> None:
        """Initialize the Bot instance with the path to the configuration file"""
        self.config_file = self.read_config_file(config_path)

    def read_config_file(self, config_path: str) -> configparser.SectionProxy:
        """Read and validate the configuration file, ensuring positive integer values"""
        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            # Ensuring positive integer values for configuration parameters
            number_of_users = int(config['CONFIG']['number_of_users'])
            max_posts_per_user = int(config['CONFIG']['max_posts_per_user'])
            max_likes_per_user = int(config['CONFIG']['max_likes_per_user'])

            if any(val <= 0 for val in [number_of_users, max_posts_per_user, max_likes_per_user]):
                raise ValueError("Invalid configuration values. Please use positive integers.")

            return config['CONFIG']

        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid configuration file. {str(e)}")

    def signup_users(self) -> list[int]:
        """Generate a list of signed-up users based on the configured number"""
        return list(range(1, int(self.config_file['number_of_users']) + 1))

    def create_posts(self, user: int) -> list[str]:
        """Create a list of posts for a given user with random sentence content"""
        posts = []
        num_posts = random.randint(1, int(self.config_file['max_posts_per_user']))

        for i in range(num_posts):
            post = f"Post by user {user} - {self.generate_random_sentence()}"
            posts.append(post)

        return posts

    def like_posts(self, posts: list[str]) -> list[str]:
        """Simulate likes on posts, determining the number and users randomly"""
        likes = []

        for post in posts:
            num_likes = random.randint(0, int(self.config_file['max_likes_per_user']))
            liked_by = random.sample(range(1, int(self.config_file['number_of_users']) + 1), num_likes)
            likes.extend([f'User {user} liked {post}' for user in liked_by])

        return likes

    def generate_random_sentence(self) -> str:
        """Generate a random sentence from parsed website with sentences"""
        amount_of_random_sentences = 10
        sentences = get_sentences(amount_of_random_sentences)
        return random.choice(sentences)

    def run(self) -> None:
        """Coordinate the execution of the bot, signing up users, creating posts and logging the results"""
        try:
            users = self.signup_users()
            all_posts = []

            for user in users:
                posts = self.create_posts(user)
                all_posts.extend(posts)

            likes = self.like_posts(all_posts)

            logger.info(f"Signed up users: {users}")
            logger.info(f"Created posts: {all_posts}")
            logger.info(f"Likes: {likes}")

        except Exception as error:
            logger.error(f"Error during bot execution: {str(error)}")


if __name__ == '__main__':
    bot = Bot('config.ini')
    bot.run()
