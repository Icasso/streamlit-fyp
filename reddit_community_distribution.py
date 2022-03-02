import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st

from database import connection, cursor


class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)
        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]
        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
               bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) is np.ndarray else [idx_min]

    def collapse(self, n_iterations=50):
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                dir_vec = self.com - self.bubbles[i, :2]
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            if i <= 8:
                ax.text(*self.bubbles[i, :2], labels[i],
                        horizontalalignment='center', verticalalignment='center')


@st.cache
def query(sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def app():
    # Main
    st.title("Reddit Community Distribution")
    st.success("Distribution of finance related subreddits")
    try:
        communities = query("""
        SELECT * FROM reddit_community_distribution
        """)

        # Sidebar
        display_amount = st.sidebar.slider("Display Amount", 2, len(communities), 8)

        subreddit = []
        subscribers = []
        color = []
        for community in communities:
            subreddit.append(community['Subreddit'])
            subscribers.append(community['Subscribers'])
            r = lambda: random.randint(0, 255)
            color.append('#%02X%02X%02X' % (r(), r(), r()))

        reddit_community_distribution = {
            'subreddit': subreddit[:display_amount],
            'subscribers': subscribers[:display_amount],
            'color': color[:display_amount]
        }

        bubble_chart = BubbleChart(area=reddit_community_distribution['subscribers'], bubble_spacing=50)
        bubble_chart.collapse()
        fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        bubble_chart.plot(ax, reddit_community_distribution['subreddit'], reddit_community_distribution['color'])
        ax.axis('off')
        ax.relim()
        ax.autoscale_view()
        st.pyplot(fig)

        reddit_community_distribution = {
            'Subreddit': subreddit[:display_amount],
            'Subscribers': subscribers[:display_amount],
        }
        df = pd.DataFrame(reddit_community_distribution)

        fig2 = px.pie(df, values='Subscribers', names='Subreddit', color_discrete_sequence=color)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Data Table")
            st.table(df)
        with col2:
            st.subheader("Pie Chart")
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""---""")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        st.warning("That date does not contain any comments after data processing, please select another date.")
        connection.rollback()
