BASE_URL = "https://leetcode.com/graphql"

QUESTION_CONTENT = """
query questionContent($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        content
        mysqlSchemas
        dataSchemas
    }
}
"""
QUESTION_TITLE = """
query questionTitle($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        isPaidOnly
        difficulty
        likes
        dislikes
        stats
    }
}

"""
SINGLE_QUESTION_TOPIC_TAGS = """
query singleQuestionTopicTags($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        topicTags {
            name
            slug
        }
    }
}
"""
QUESTION_DETAIL_COMPANY_TAGS = """
query questionDetailCompanyTags($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        companyTags {
            name
            slug
            imgUrl
        }
    }
} 
"""
COMMUNITY_SOLUTIONS = """
query communitySolutions($titleSlug: String!, $skip: Int!, $first: Int!, $query: String, $orderBy: TopicSortingOption, $languageTags: [String!], $topicTags: [String!]) {
    questionSolutions(
        filters: {questionSlug: $titleSlug, skip: $skip, first: $first, query: $query, orderBy: $orderBy, languageTags: $languageTags, topicTags: $topicTags}
    ) {
        hasDirectResults
        totalNum
        solutions {
            id
            title
            commentCount
            topLevelCommentCount
            viewCount
            pinned
            isFavorite
            solutionTags {
                name
                slug
            }
        }
    }
}
"""
