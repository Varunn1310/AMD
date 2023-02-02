#include "squareroot.cpp"
#include <gtest/gtest.h>

TEST(SquareRootTest, PositiveNos) { 
    //Expect operations
    EXPECT_EQ(12, SquareRoot(144.0));
    EXPECT_EQ(5, SquareRoot(122.0));
    EXPECT_TRUE(12 == SquareRoot(144.0));
    EXPECT_FALSE(5 != SquareRoot(122.0));
    //Assert operations
    ASSERT_EQ(6, SquareRoot(36.0));
    ASSERT_EQ(18.0, SquareRoot(324.0));
    ASSERT_TRUE(25.4 == SquareRoot(645.16));
    ASSERT_FALSE(25.4 != SquareRoot(645.16));
    ASSERT_EQ(0, SquareRoot(0.0));
    //String assertions
    ASSERT_STREQ("Hello", "Hello");
    ASSERT_STRNE("Hello", "Hi");
}

TEST(SquareRootTest, NegativeNos) {
    EXPECT_EQ(-12, SquareRoot(-144.0));
    EXPECT_EQ(-5, SquareRoot(-122.0));
    ASSERT_EQ(-1.0, SquareRoot(-15.0));
    ASSERT_EQ(-1.0, SquareRoot(-0.2));
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}