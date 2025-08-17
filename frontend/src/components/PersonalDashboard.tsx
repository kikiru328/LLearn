// src/components/PersonalDashboard.tsx - 수정된 버전
import {
  Box,
  Button,
  VStack,
  HStack,
  Heading,
  Container,
  Text,
  useColorModeValue,
  Card,
  CardBody,
  Grid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Badge,
  Avatar,
  Spinner,
  SimpleGrid,
  Icon,
  Alert,
  AlertIcon,
  AlertDescription,
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { AddIcon, ViewIcon, StarIcon } from '@chakra-ui/icons';
import { 
  RssIcon, 
  HeartIcon, 
  BookmarkIcon, 
  UsersIcon,
  CommentIcon
} from './icons/SimpleIcons';
import { 
  curriculumAPI, 
  summaryAPI, 
  feedbackAPI, 
  followAPI, 
  userAPI 
} from '../services/api';
import { getCurrentUserId } from '../utils/auth';

interface DashboardStats {
  curriculumCount: number;
  summaryCount: number;
  feedbackCount: number;
  avgScore: number | null;
  followersCount: number;
  followingCount: number;
  recentCurriculums: Array<{
    id: string;
    title: string;
    total_weeks: number;
    created_at: string;
  }>;
  recentSummaries: Array<{
    id: string;
    curriculum_title?: string;
    week_number: number;
    created_at: string;
  }>;
}

interface UserProfile {
  name: string;
  email: string;
}

const PersonalDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  
  const textColor = useColorModeValue('gray.900', 'white');
  const secondaryTextColor = useColorModeValue('gray.600', 'gray.300');
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const statBg = useColorModeValue('blue.50', 'blue.900');
  const highlightBg = useColorModeValue('gray.50', 'gray.800');
  const hoverBg = useColorModeValue('gray.100', 'gray.600');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    console.log('대시보드 데이터 로드 시작...');
    
    const currentUserId = getCurrentUserId();
    console.log('현재 사용자 ID:', currentUserId);
    
    if (!currentUserId) {
      setError('사용자 인증이 필요합니다');
      setLoading(false);
      return;
    }

    // 1. 사용자 프로필 조회
    try {
      console.log('프로필 조회 중...');
      const profileResponse = await userAPI.getProfile();
      console.log('프로필 응답:', profileResponse.data);
      setProfile(profileResponse.data);
    } catch (error) {
      console.error('프로필 조회 실패:', error);
      setProfile({ name: '사용자', email: '' });
    }
    
    // 2. 커리큘럼 데이터 조회
    let curriculumCount = 0;
    let recentCurriculums: any[] = [];
    try {
      console.log('커리큘럼 조회 중...');
      const curriculumResponse = await curriculumAPI.getAll({ page: 1, items_per_page: 5 });
      console.log('커리큘럼 원본 응답:', curriculumResponse);
      console.log('커리큘럼 데이터:', curriculumResponse.data);
      
      // 응답 구조 확인 및 안전한 접근
      if (curriculumResponse.data) {
        // 다양한 응답 형태에 대응
        if (curriculumResponse.data.curriculums) {
          curriculumCount = curriculumResponse.data.total_count || curriculumResponse.data.curriculums.length;
          recentCurriculums = curriculumResponse.data.curriculums.slice(0, 3);
        } else if (Array.isArray(curriculumResponse.data)) {
          curriculumCount = curriculumResponse.data.length;
          recentCurriculums = curriculumResponse.data.slice(0, 3);
        } else {
          console.warn('예상하지 못한 커리큘럼 응답 구조:', curriculumResponse.data);
        }
      }
      console.log('처리된 커리큘럼 카운트:', curriculumCount);
      console.log('최근 커리큘럼:', recentCurriculums);
    } catch (error) {
      console.error('커리큘럼 조회 실패:', error);
    }

    // 3. 요약 데이터 조회 및 커리큘럼 제목 매핑
    let summaryCount = 0;
    let recentSummaries: any[] = [];
    try {
      console.log('요약 조회 중...');
      const summaryResponse = await summaryAPI.getAll({ page: 1, items_per_page: 5 });
      console.log('요약 원본 응답:', summaryResponse);
      console.log('요약 데이터:', summaryResponse.data);
      
      if (summaryResponse.data) {
        let summaries = [];
        if (summaryResponse.data.summaries) {
          summaryCount = summaryResponse.data.total_count || summaryResponse.data.summaries.length;
          summaries = summaryResponse.data.summaries.slice(0, 3);
        } else if (Array.isArray(summaryResponse.data)) {
          summaryCount = summaryResponse.data.length;
          summaries = summaryResponse.data.slice(0, 3);
        }

        // 각 요약에 대해 커리큘럼 제목 가져오기
        recentSummaries = await Promise.all(
          summaries.map(async (summary: any) => {
            let curriculumTitle = summary.curriculum_title || '제목 없음';
            
            // curriculum_title이 없다면 커리큘럼 API로 조회
            if (!summary.curriculum_title && summary.curriculum_id) {
              try {
                // 이미 가져온 커리큘럼 데이터에서 찾기
                const matchingCurriculum = recentCurriculums.find(c => c.id === summary.curriculum_id);
                if (matchingCurriculum) {
                  curriculumTitle = matchingCurriculum.title;
                } else {
                  // 개별 커리큘럼 조회
                  const curriculumResponse = await curriculumAPI.getById(summary.curriculum_id);
                  curriculumTitle = curriculumResponse.data.title;
                }
              } catch (error) {
                console.error(`커리큘럼 제목 조회 실패 (${summary.curriculum_id}):`, error);
                curriculumTitle = `${summary.week_number}주차 학습`;
              }
            }
            
            return {
              ...summary,
              curriculum_title: curriculumTitle
            };
          })
        );
      }
      console.log('처리된 요약 카운트:', summaryCount);
      console.log('커리큘럼 제목이 포함된 최근 요약:', recentSummaries);
    } catch (error) {
      console.error('요약 조회 실패:', error);
    }

    // 4. 피드백 데이터 조회 - 400 에러 처리
    let feedbackCount = 0;
    let avgScore = null;
    try {
      console.log('피드백 조회 중...');
      const feedbackResponse = await feedbackAPI.getAll({ page: 1, items_per_page: 100 });
      console.log('피드백 원본 응답:', feedbackResponse);
      console.log('피드백 데이터:', feedbackResponse.data);
      
      if (feedbackResponse.data) {
        let feedbacks = [];
        if (feedbackResponse.data.feedbacks) {
          feedbacks = feedbackResponse.data.feedbacks;
        } else if (Array.isArray(feedbackResponse.data)) {
          feedbacks = feedbackResponse.data;
        }
        
        feedbackCount = feedbacks.length;
        if (feedbacks.length > 0) {
          const totalScore = feedbacks.reduce((sum: number, fb: any) => sum + (fb.score || 0), 0);
          avgScore = totalScore / feedbacks.length;
        }
      }
      console.log('처리된 피드백 카운트:', feedbackCount);
      console.log('평균 점수:', avgScore);
    } catch (error: any) {
      console.error('피드백 조회 실패:', error);
      // 400 에러는 피드백 기능이 구현되지 않았거나 데이터가 없는 것으로 처리
      if (error.response?.status === 400) {
        console.log('피드백 기능이 아직 구현되지 않음 또는 데이터 없음');
      }
    }

    // 5. 팔로우 통계 조회
    let followersCount = 0;
    let followingCount = 0;
    try {
      console.log('팔로우 통계 조회 중...');
      const followStats = await followAPI.getFollowStats(currentUserId);
      console.log('팔로우 통계 응답:', followStats.data);
      followersCount = followStats.data.followers_count || 0;
      followingCount = followStats.data.followees_count || 0;
    } catch (error) {
      console.error('팔로우 통계 조회 실패:', error);
      // 팔로우 기능이 없을 수도 있으므로 경고로만 처리
    }

    // 6. 최종 통계 설정 - 항상 실행
    const finalStats = {
      curriculumCount,
      summaryCount,
      feedbackCount,
      avgScore,
      followersCount,
      followingCount,
      recentCurriculums,
      recentSummaries,
    };

    console.log('최종 통계:', finalStats);
    setStats(finalStats);
    setLoading(false);
  };

  const quickActions = [
    {
      title: '새 커리큘럼',
      description: 'AI가 맞춤형 커리큘럼을 생성해드립니다',
      icon: AddIcon,
      color: 'blue',
      action: () => navigate('/curriculum'),
    },
    {
      title: '학습 요약',
      description: '오늘 학습한 내용을 요약해보세요',
      icon: StarIcon,
      color: 'green',
      action: () => navigate('/summary'),
    },
    {
      title: '커뮤니티 피드',
      description: '다른 사용자들의 학습 여정을 둘러보세요',
      icon: RssIcon,
      color: 'purple',
      action: () => navigate('/feed'),
    },
  ];

  if (loading) {
    return (
      <Container maxW="6xl" py={8}>
        <VStack spacing={4}>
          <Spinner size="xl" color="blue.500" />
          <Text color={textColor}>대시보드를 불러오는 중...</Text>
        </VStack>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxW="6xl" py={8}>
        <Alert status="error" mb={4}>
          <AlertIcon />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button onClick={fetchDashboardData} colorScheme="blue">
          다시 시도
        </Button>
      </Container>
    );
  }

  return (
    <Container maxW="6xl" py={8}>
      <VStack spacing={8} align="stretch">
        {/* 환영 메시지 */}
        <HStack justify="space-between" align="center">
          <VStack align="start" spacing={1}>
            <Heading size="lg" color={textColor}>
              안녕하세요, {profile?.name || '사용자'}님! 👋
            </Heading>
            <Text color={secondaryTextColor}>
              오늘도 성장하는 하루 되세요!
            </Text>
          </VStack>
          <Avatar name={profile?.name || '사용자'} size="lg" />
        </HStack>

        {/* 통계 카드 */}
        <SimpleGrid columns={{ base: 2, md: 4, lg: 6 }} spacing={4}>
          <Stat textAlign="center" bg={statBg} p={4} borderRadius="md">
            <StatLabel color={secondaryTextColor}>커리큘럼</StatLabel>
            <StatNumber color={textColor}>{stats?.curriculumCount || 0}</StatNumber>
            <StatHelpText color={secondaryTextColor}>개 생성</StatHelpText>
          </Stat>
          
          <Stat textAlign="center" bg={highlightBg} p={4} borderRadius="md">
            <StatLabel color={secondaryTextColor}>학습 요약</StatLabel>
            <StatNumber color={textColor}>{stats?.summaryCount || 0}</StatNumber>
            <StatHelpText color={secondaryTextColor}>개 작성</StatHelpText>
          </Stat>
          
          <Stat textAlign="center" bg={highlightBg} p={4} borderRadius="md">
            <StatLabel color={secondaryTextColor}>AI 피드백</StatLabel>
            <StatNumber color={textColor}>{stats?.feedbackCount || 0}</StatNumber>
            <StatHelpText color={secondaryTextColor}>
              {stats?.avgScore ? `평균 ${stats.avgScore.toFixed(1)}점` : '점수 없음'}
            </StatHelpText>
          </Stat>
          
          <Stat 
            textAlign="center" 
            bg={statBg} 
            p={4} 
            borderRadius="md"
            cursor="pointer"
            _hover={{ transform: 'scale(1.02)' }}
            onClick={() => navigate('/social/follow?tab=followers')}
          >
            <StatLabel color={secondaryTextColor}>팔로워</StatLabel>
            <StatNumber color={textColor}>{stats?.followersCount || 0}</StatNumber>
            <StatHelpText color={secondaryTextColor}>명</StatHelpText>
          </Stat>
          
          <Stat 
            textAlign="center" 
            bg={statBg} 
            p={4} 
            borderRadius="md"
            cursor="pointer"
            _hover={{ transform: 'scale(1.02)' }}
            onClick={() => navigate('/social/follow?tab=following')}
          >
            <StatLabel color={secondaryTextColor}>팔로잉</StatLabel>
            <StatNumber color={textColor}>{stats?.followingCount || 0}</StatNumber>
            <StatHelpText color={secondaryTextColor}>명</StatHelpText>
          </Stat>

          <Stat textAlign="center" bg={highlightBg} p={4} borderRadius="md">
            <StatLabel color={secondaryTextColor}>총 활동</StatLabel>
            <StatNumber color={textColor}>
              {(stats?.curriculumCount || 0) + (stats?.summaryCount || 0)}
            </StatNumber>
            <StatHelpText color={secondaryTextColor}>개</StatHelpText>
          </Stat>
        </SimpleGrid>

        {/* 빠른 실행 */}
        <Card bg={cardBg} borderColor={borderColor}>
          <CardBody>
            <VStack spacing={4}>
              <Heading size="md" color={textColor} alignSelf="start">
                빠른 실행
              </Heading>
              <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={4} w="100%">
                {quickActions.map((action, index) => (
                  <Button
                    key={index}
                    height="80px"
                    variant="outline"
                    colorScheme={action.color}
                    onClick={action.action}
                    _hover={{ transform: 'translateY(-2px)', shadow: 'md' }}
                    transition="all 0.2s"
                  >
                    <VStack spacing={2}>
                      <Icon as={action.icon} boxSize={5} />
                      <Text fontWeight="bold" fontSize="sm">
                        {action.title}
                      </Text>
                      <Text fontSize="xs" color={secondaryTextColor} noOfLines={2}>
                        {action.description}
                      </Text>
                    </VStack>
                  </Button>
                ))}
              </Grid>
            </VStack>
          </CardBody>
        </Card>

        {/* 최근 활동 */}
        <Grid templateColumns={{ base: '1fr', lg: '1fr 1fr' }} gap={6}>
          {/* 최근 커리큘럼 */}
          <Card bg={cardBg} borderColor={borderColor}>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack justify="space-between">
                  <Heading size="md" color={textColor}>최근 커리큘럼</Heading>
                  <Button size="sm" variant="ghost" onClick={() => navigate('/curriculum')}>
                    전체보기
                  </Button>
                </HStack>
                
                {stats?.recentCurriculums && stats.recentCurriculums.length > 0 ? (
                  <VStack spacing={3} align="stretch">
                    {stats.recentCurriculums.map((curriculum) => (
                      <Box
                        key={curriculum.id}
                        p={3}
                        bg={highlightBg}
                        borderRadius="md"
                        cursor="pointer"
                        _hover={{ bg: hoverBg }}
                        onClick={() => navigate(`/curriculum/${curriculum.id}`)}
                      >
                        <VStack align="start" spacing={1}>
                          <Text fontWeight="semibold" color={textColor} noOfLines={1}>
                            {curriculum.title}
                          </Text>
                          <HStack spacing={2}>
                            <Badge colorScheme="blue" size="sm">
                              {curriculum.total_weeks}주차
                            </Badge>
                            <Text fontSize="xs" color={secondaryTextColor}>
                              {new Date(curriculum.created_at).toLocaleDateString()}
                            </Text>
                          </HStack>
                        </VStack>
                      </Box>
                    ))}
                  </VStack>
                ) : (
                  <Box textAlign="center" py={6}>
                    <Text color={secondaryTextColor} mb={3}>
                      아직 커리큘럼이 없습니다
                    </Text>
                    <Button size="sm" colorScheme="blue" onClick={() => navigate('/curriculum')}>
                      첫 커리큘럼 만들기
                    </Button>
                  </Box>
                )}
              </VStack>
            </CardBody>
          </Card>

          {/* 최근 요약 */}
          <Card bg={cardBg} borderColor={borderColor}>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <HStack justify="space-between">
                  <Heading size="md" color={textColor}>최근 학습 요약</Heading>
                  <Button size="sm" variant="ghost" onClick={() => navigate('/summary')}>
                    전체보기
                  </Button>
                </HStack>
                
                {stats?.recentSummaries && stats.recentSummaries.length > 0 ? (
                  <VStack spacing={3} align="stretch">
                    {stats.recentSummaries.map((summary) => (
                      <Box
                        key={summary.id}
                        p={3}
                        bg={highlightBg}
                        borderRadius="md"
                        cursor="pointer"
                        _hover={{ bg: hoverBg }}
                        onClick={() => navigate(`/summary/${summary.id}`)}
                      >
                        <VStack align="start" spacing={1}>
                          <Text fontWeight="semibold" color={textColor} noOfLines={1}>
                            {summary.curriculum_title || '제목 없음'}
                          </Text>
                          <HStack spacing={2}>
                            <Badge colorScheme="green" size="sm">
                              {summary.week_number}주차
                            </Badge>
                            <Text fontSize="xs" color={secondaryTextColor}>
                              {new Date(summary.created_at).toLocaleDateString()}
                            </Text>
                          </HStack>
                        </VStack>
                      </Box>
                    ))}
                  </VStack>
                ) : (
                  <Box textAlign="center" py={6}>
                    <Text color={secondaryTextColor} mb={3}>
                      아직 학습 요약이 없습니다
                    </Text>
                    <Button size="sm" colorScheme="green" onClick={() => navigate('/summary')}>
                      첫 요약 작성하기
                    </Button>
                  </Box>
                )}
              </VStack>
            </CardBody>
          </Card>
        </Grid>
      </VStack>
    </Container>
  );
};

export default PersonalDashboard;
