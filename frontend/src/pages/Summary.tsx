// src/pages/Summary.tsx - 완전한 이모지 버전
import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  VStack,
  HStack,
  Heading,
  Container,
  Text,
  Card,
  CardBody,
  Badge,
  useToast,
  Spinner,
  Alert,
  AlertIcon,
  AlertDescription,
  useColorModeValue,
  Grid,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Textarea,
  FormControl,
  FormLabel,
  Select,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
} from '@chakra-ui/react';
import { 
  AddIcon, 
  EditIcon, 
  DeleteIcon,
  StarIcon,
  CheckIcon,
  TimeIcon,
  ChatIcon,
} from '@chakra-ui/icons';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { summaryAPI, curriculumAPI, feedbackAPI } from '../services/api';
import { getCurrentUserId } from '../utils/auth';

interface Summary {
  id: string;
  curriculum_id: string;
  week_number: number;
  content: string;
  content_length: number;
  snippet: string;
  created_at: string;
  updated_at: string;
}

interface WeekSchedule {
  week_number: number;
  title?: string; 
  lessons?: string[];
}

interface Curriculum {
  id: string;
  owner_id: string;
  title: string;
  total_weeks: number;
  week_schedules?: WeekSchedule[];
}

interface SummaryForm {
  curriculum_id: string;
  week_number: number;
  content: string;
}

interface Feedback {
  id: string;
  summary_id: string;
  comment: string;
  score: number;
  grade: string;
  created_at: string;
}

const Summary: React.FC = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [searchParams] = useSearchParams();
  
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [curriculums, setCurriculums] = useState<Curriculum[]>([]);
  const [selectedCurriculum, setSelectedCurriculum] = useState<Curriculum | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [editingSummary, setEditingSummary] = useState<Summary | null>(null);
  const [summaryForm, setSummaryForm] = useState<SummaryForm>({
    curriculum_id: '',
    week_number: 1,
    content: ''
  });
  const [currentView, setCurrentView] = useState<'create' | 'list'>('list');
  const [feedbacks, setFeedbacks] = useState<Record<string, Feedback>>({});
  const [loadingFeedbacks, setLoadingFeedbacks] = useState<Record<string, boolean>>({});
  
  const { isOpen: isCreateModalOpen, onOpen: onCreateModalOpen, onClose: onCreateModalClose } = useDisclosure();
  const { isOpen: isEditModalOpen, onOpen: onEditModalOpen, onClose: onEditModalClose } = useDisclosure();
  
  // 다크모드 대응 색상
  const textColor = useColorModeValue('gray.900', 'white');
  const secondaryTextColor = useColorModeValue('gray.600', 'gray.300');
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  useEffect(() => {
    initializePage();
  }, [searchParams]);

  const initializePage = async () => {
    // URL 파라미터에서 정보 가져오기
    const curriculumId = searchParams.get('curriculum_id');
    const weekNumber = searchParams.get('week_number');
    const lessonIndex = searchParams.get('lesson_index');
    const view = searchParams.get('view');

    await fetchData();

    if (curriculumId && weekNumber) {
      setSummaryForm(prev => ({
        ...prev,
        curriculum_id: curriculumId,
        week_number: parseInt(weekNumber),
      }));

      if (view === 'list') {
        // 요약 목록 보기 모드
        setCurrentView('list');
        await fetchSummariesByCurriculumAndWeek(curriculumId, parseInt(weekNumber));
      }
    }
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      setError('');
      
      // 내 커리큘럼만 조회 (이미 올바른 엔드포인트 사용 중)
      const [curriculumResponse, summaryResponse] = await Promise.all([
        curriculumAPI.getAll(), // 이미 '/curriculums/me' 엔드포인트 사용
        summaryAPI.getAll()     // 이미 '/users/me/summaries' 엔드포인트 사용
      ]);
      
      const curriculumData = curriculumResponse.data.curriculums || [];
      setCurriculums(curriculumData);

      const summaryData = summaryResponse.data.summaries || [];
      setSummaries(summaryData);

      await loadFeedbacksForSummaries(summaryData);
    } catch (error: any) {
      console.error('데이터 조회 실패:', error);
      setError('데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const fetchSummariesByCurriculumAndWeek = async (curriculumId: string, weekNumber: number) => {
    try {
      const response = await summaryAPI.getByWeek(curriculumId, weekNumber);
      setSummaries(response.data.summaries || []);
      
      // 선택된 커리큘럼 정보 설정
      const curriculum = curriculums.find(c => c.id === curriculumId);
      setSelectedCurriculum(curriculum || null);
    } catch (error: any) {
      console.error('주차별 요약 조회 실패:', error);
      toast({
        title: '😕 요약을 불러오는데 실패했습니다',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const handleCreateSummary = async () => {
    if (!summaryForm.curriculum_id || !summaryForm.content.trim()) {
      toast({
        title: '📝 필수 정보를 입력해주세요',
        status: 'warning',
        duration: 3000,
      });
      return;
    }
    const selectedCurriculum = curriculums.find(c => c.id === summaryForm.curriculum_id);
    const currentUserId = getCurrentUserId();

    if (!selectedCurriculum || selectedCurriculum.owner_id !== currentUserId) {
      toast({
        title: '🚫 권한이 없습니다',
        description: '본인의 커리큘럼에만 요약을 작성할 수 있습니다.',
        status: 'error',
        duration: 3000,
      });
      return;
    }
    try {
      setSubmitting(true);
      await summaryAPI.create({
        curriculum_id: summaryForm.curriculum_id,
        week_number: summaryForm.week_number,
        content: summaryForm.content.trim()
      });
      
      toast({
        title: '✨ 요약이 저장되었습니다!',
        status: 'success',
        duration: 3000,
      });
      
      setSummaryForm({
        curriculum_id: '',
        week_number: 1,
        content: ''
      });
      onCreateModalClose();
      fetchData();
    } catch (error: any) {
      console.error('요약 생성 실패:', error);
      toast({
        title: '😕 요약 저장에 실패했습니다',
        description: error.response?.data?.detail || '다시 시도해주세요',
        status: 'error',
        duration: 5000,
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleEditSummary = async (summary: Summary) => {
    setEditingSummary(summary);
    
    // 먼저 커리큘럼 상세 정보 로드
    try {
      const curriculum = curriculums.find(c => c.id === summary.curriculum_id);
      if (!curriculum || !curriculum.week_schedules) {
        console.log('커리큘럼 상세 정보 로드 중...');
        const response = await curriculumAPI.getById(summary.curriculum_id);
        const detailedCurriculum = response.data;
        
        // curriculums 업데이트
        setCurriculums(prev => 
          prev.map(c => 
            c.id === summary.curriculum_id 
              ? { ...c, week_schedules: detailedCurriculum.week_schedules }
              : c
          )
        );
      }
    } catch (error) {
      console.error('커리큘럼 상세 정보 로드 실패:', error);
    }
    
    setSummaryForm({
      curriculum_id: summary.curriculum_id,
      week_number: summary.week_number,
      content: summary.content
    });
    
    onEditModalOpen();
  };

  const handleUpdateSummary = async () => {
    if (!editingSummary || !summaryForm.content.trim()) {
      toast({
        title: '📝 내용을 입력해주세요',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    try {
      setSubmitting(true);
      await summaryAPI.update(editingSummary.id, {
        content: summaryForm.content.trim()
      });
      
      toast({
        title: '✨ 요약이 수정되었습니다!',
        status: 'success',
        duration: 3000,
      });
      
      onEditModalClose();
      fetchData();
    } catch (error: any) {
      console.error('요약 수정 실패:', error);
      toast({
        title: '😕 요약 수정에 실패했습니다',
        status: 'error',
        duration: 3000,
      });
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteSummary = async (summaryId: string) => {
    if (!window.confirm('🗑️ 정말로 이 요약을 삭제하시겠습니까?')) {
      return;
    }

    try {
      await summaryAPI.delete(summaryId);
      
      toast({
        title: '🗑️ 요약이 삭제되었습니다',
        status: 'success',
        duration: 3000,
      });
      
      fetchData();
    } catch (error: any) {
      console.error('요약 삭제 실패:', error);
      toast({
        title: '😕 요약 삭제에 실패했습니다',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const getCurriculumTitle = (curriculumId: string) => {
    const curriculum = curriculums.find(c => c.id === curriculumId);
    return curriculum?.title || '❓ 알 수 없는 커리큘럼';
  };

  // 피드백 로드 함수
  const loadFeedbacksForSummaries = async (summaryList: Summary[]) => {
    const feedbackPromises = summaryList.map(async (summary) => {
      try {
        const response = await feedbackAPI.getBySummary(summary.id);
        return { summaryId: summary.id, feedback: response.data };
      } catch (error) {
        return { summaryId: summary.id, feedback: null };
      }
    });

    const results = await Promise.all(feedbackPromises);
    const feedbackMap: Record<string, Feedback> = {};
    
    results.forEach(({ summaryId, feedback }) => {
      if (feedback) {
        feedbackMap[summaryId] = feedback;
      }
    });
    
    setFeedbacks(feedbackMap);
  };

  // 피드백 요청 함수
  const handleRequestFeedback = async (summaryId: string) => {
    try {
      setLoadingFeedbacks(prev => ({ ...prev, [summaryId]: true }));
      
      await feedbackAPI.generateFeedback(summaryId);
      
      toast({
        title: '🤖 피드백 생성을 요청했습니다',
        description: '잠시 후 AI가 분석한 피드백이 생성됩니다 ⏳',
        status: 'success',
        duration: 3000,
      });
      
      // 피드백 생성 후 다시 로드
      setTimeout(async () => {
        try {
          const response = await feedbackAPI.getBySummary(summaryId);
          setFeedbacks(prev => ({ ...prev, [summaryId]: response.data }));
        } catch (error) {
          // 아직 생성 중일 수 있음
        }
        setLoadingFeedbacks(prev => ({ ...prev, [summaryId]: false }));
      }, 2000);
      
    } catch (error: any) {
      console.error('피드백 요청 실패:', error);
      toast({
        title: '😕 피드백 요청에 실패했습니다',
        status: 'error',
        duration: 3000,
      });
      setLoadingFeedbacks(prev => ({ ...prev, [summaryId]: false }));
    }
  };

  // 피드백 상태 확인 함수 - 개선된 버전
  const getFeedbackStatus = (summaryId: string) => {
    if (loadingFeedbacks[summaryId]) {
      return { status: 'loading', label: '🤖 생성 중...', color: 'yellow' };
    }
    
    if (feedbacks[summaryId]) {
      const feedback = feedbacks[summaryId];
      const score = feedback.score;
      
      if (score >= 9) return { status: 'completed', label: '🏆 탁월', color: 'purple' };
      if (score >= 8) return { status: 'completed', label: '🌟 우수', color: 'blue' };
      if (score >= 7) return { status: 'completed', label: '👍 양호', color: 'green' };
      if (score >= 6) return { status: 'completed', label: '📚 보통', color: 'yellow' };
      if (score >= 5) return { status: 'completed', label: '📝 미흡', color: 'orange' };
      return { status: 'completed', label: '💪 노력필요', color: 'red' };
    }
    
    return { status: 'none', label: '🎯 피드백 요청', color: 'gray' };
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // 선택된 커리큘럼의 주차 목록 생성 (week_schedules가 없어도 total_weeks 기반으로 생성)
  const getSelectedCurriculumWeeks = () => {
    console.log('=== getSelectedCurriculumWeeks 호출됨 ===');
    console.log('summaryForm.curriculum_id:', summaryForm.curriculum_id);
    
    if (!summaryForm.curriculum_id) {
      console.log('curriculum_id가 없음');
      return [];
    }
    
    const curriculum = curriculums.find(c => c.id === summaryForm.curriculum_id);
    console.log('찾은 커리큘럼:', curriculum);
    
    if (!curriculum) {
      console.log('커리큘럼을 찾지 못함');
      return [];
    }

    console.log('week_schedules:', curriculum.week_schedules);
    console.log('total_weeks:', curriculum.total_weeks);

    // 안전장치 추가
    if (curriculum.week_schedules && Array.isArray(curriculum.week_schedules) && curriculum.week_schedules.length > 0) {
      console.log('실제 week_schedules 사용');
      return curriculum.week_schedules;
    } else if (curriculum.total_weeks && curriculum.total_weeks > 0) {
      console.log('임시 데이터 생성');
      return Array.from({ length: curriculum.total_weeks }, (_, index) => ({
        week_number: index + 1,
        title: `${index + 1}주차 학습`,
        lessons: [`${index + 1}주차 학습 내용`]
      }));
    }
    
    console.log('빈 배열 반환');
    return [] as WeekSchedule[];
  };

  const getWeekTitle = (curriculumId: string, weekNumber: number) => {
    const curriculum = curriculums.find(c => c.id === curriculumId);
    if (!curriculum || !curriculum.week_schedules) {
      return `📅 ${weekNumber}주차`;
    }
    
    const week = curriculum.week_schedules.find(w => w.week_number === weekNumber);
    return week?.title ? `📅 ${weekNumber}주차: ${week.title}` : `📅 ${weekNumber}주차`;
  };

  const getSelectedWeekLessons = () => {
    try {
      const weeks = getSelectedCurriculumWeeks();
      console.log('getSelectedWeekLessons - weeks:', weeks);
      
      if (!weeks || !Array.isArray(weeks) || weeks.length === 0) {
        console.log('weeks가 유효하지 않음:', weeks);
        return [];
      }
      
      const week = weeks.find(w => w && w.week_number === summaryForm.week_number);
      console.log('getSelectedWeekLessons - 찾은 week:', week);
      
      if (!week) {
        console.log('주차를 찾을 수 없음');
        return [];
      }
      
      if (!week.lessons || !Array.isArray(week.lessons)) {
        console.log('lessons가 유효하지 않음:', week.lessons);
        return [];
      }
      
      return Array.isArray(week.lessons) ? week.lessons : [];
    } catch (error) {
      console.error('getSelectedWeekLessons 에러:', error);
      return []; // 항상 배열 반환 보장
    }
  };

  if (loading) {
    return (
      <Container maxW="6xl" py={8}>
        <VStack spacing={4}>
          <Spinner size="xl" color="blue.500" />
          <Text color={textColor}>📖 요약을 불러오는 중...</Text>
        </VStack>
      </Container>
    );
  }

  return (
    <Container maxW="6xl" py={8}>
      <VStack spacing={6} align="stretch">
        {/* 브레드크럼 */}
        <Breadcrumb color={secondaryTextColor}>
          <BreadcrumbItem>
            <BreadcrumbLink onClick={() => navigate('/')}>
              🏠 홈
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbItem isCurrentPage>
            <BreadcrumbLink color={textColor}>📚 학습 요약</BreadcrumbLink>
          </BreadcrumbItem>
        </Breadcrumb>

        {/* 헤더 */}
        <HStack justify="space-between" align="center">
          <Heading size="lg" color={textColor}>
            {selectedCurriculum ? `📖 ${selectedCurriculum.title} - 요약` : '📚 학습 요약'}
          </Heading>
          <HStack>
            {selectedCurriculum && (
              <Button
                variant="outline"
                onClick={() => {
                  setCurrentView('list');
                  setSelectedCurriculum(null);
                  fetchData();
                }}
              >
                📋 전체 보기
              </Button>
            )}
            <Button
              leftIcon={<AddIcon />}
              colorScheme="blue"
              onClick={onCreateModalOpen}
            >
              📝 새 요약 작성
            </Button>
          </HStack>
        </HStack>

        {/* 에러 메시지 */}
        {error && (
          <Alert status="error">
            <AlertIcon />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* 요약 목록 */}
        {(summaries?.length ?? 0) === 0 ? (
          <Card bg={cardBg} borderColor={borderColor}>
            <CardBody>
              <VStack spacing={4} py={8}>
                <Text fontSize="4xl">📝</Text>
                <Heading size="md" color={secondaryTextColor}>
                  {selectedCurriculum ? '📖 이 커리큘럼에는 아직 작성된 요약이 없습니다' : '📚 아직 작성된 요약이 없습니다'}
                </Heading>
                <Text color={secondaryTextColor} textAlign="center">
                  학습한 내용을 요약해보세요! ✨<br />
                  요약을 통해 학습 내용을 더 잘 기억할 수 있습니다. 🧠
                </Text>
                <Button
                  leftIcon={<AddIcon />}
                  colorScheme="blue"
                  onClick={onCreateModalOpen}
                  size="lg"
                >
                  📝 첫 번째 요약 작성하기
                </Button>
              </VStack>
            </CardBody>
          </Card>
        ) : (
          <Grid templateColumns="repeat(auto-fill, minmax(350px, 1fr))" gap={6}>
            {summaries.map((summary) => (
              <Card 
                key={summary.id} 
                variant="outline" 
                bg={cardBg} 
                borderColor={borderColor}
                cursor="pointer"
                transition="all 0.2s"
                _hover={{ 
                  transform: "translateY(-2px)", 
                  shadow: "lg",
                  borderColor: "blue.300"
                }}
                onClick={() => navigate(`/summary/${summary.id}`)}
              >
                <CardBody>
                  <VStack align="stretch" spacing={3}>
                    {/* 헤더 */}
                    <VStack align="start" spacing={1}>
                      <Text fontSize="sm" color="blue.500" fontWeight="semibold">
                        📖 {getCurriculumTitle(summary.curriculum_id)}
                      </Text>
                      <Heading size="sm" color={textColor} noOfLines={1}>
                        {getWeekTitle(summary.curriculum_id, summary.week_number)}
                      </Heading>
                      <HStack>
                        <Badge colorScheme="blue" variant="subtle" size="sm">
                          📅 {summary.week_number}주차
                        </Badge>
                        {(() => {
                          const feedbackStatus = getFeedbackStatus(summary.id);
                          return (
                            <Badge 
                              colorScheme={feedbackStatus.color} 
                              variant={feedbackStatus.status === 'completed' ? 'solid' : 'outline'}
                              size="sm"
                            >
                              {feedbackStatus.status === 'loading' && <TimeIcon mr={1} />}
                              {feedbackStatus.status === 'completed' && <CheckIcon mr={1} />}
                              {feedbackStatus.label}
                            </Badge>
                          );
                        })()}
                      </HStack>
                    </VStack>
                    {/* 요약 내용 미리보기 */}
                    <Text 
                      color={secondaryTextColor} 
                      fontSize="sm" 
                      noOfLines={3}
                      minH="60px"
                    >
                      {summary.snippet}
                    </Text>

                    {/* 메타 정보 */}
                    <Text fontSize="xs" color={secondaryTextColor}>
                      📅 {formatDate(summary.created_at)}
                      {summary.updated_at !== summary.created_at && ' ✏️ (수정됨)'}
                    </Text>

                    {/* 액션 버튼 */}
                    <HStack spacing={2} justify="flex-end">
                      {getFeedbackStatus(summary.id).status === 'none' && (
                        <Button
                          leftIcon={<ChatIcon />}
                          size="sm"
                          variant="ghost"
                          colorScheme="green"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleRequestFeedback(summary.id);
                          }}
                        >
                          🤖 피드백 요청
                        </Button>
                      )}
                      <Button
                        leftIcon={<EditIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="blue"
                        onClick={(e) => {
                          e.stopPropagation(); // 카드 클릭 이벤트 방지
                          handleEditSummary(summary);
                        }}
                      >
                        ✏️ 수정
                      </Button>
                      <Button
                        leftIcon={<DeleteIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="red"
                        onClick={(e) => {
                          e.stopPropagation(); // 카드 클릭 이벤트 방지
                          handleDeleteSummary(summary.id);
                        }}
                      >
                        🗑️ 삭제
                      </Button>
                    </HStack>
                  </VStack>
                </CardBody>
              </Card>
            ))}
          </Grid>
        )}

        {/* 요약 작성 모달 */}
        <Modal isOpen={isCreateModalOpen} onClose={onCreateModalClose} size="xl">
          <ModalOverlay />
          <ModalContent bg={cardBg} color={textColor}>
            <ModalHeader>📝 새 요약 작성</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel color={textColor}>📚 커리큘럼 선택</FormLabel>
                  <Select
                    placeholder="📖 내 커리큘럼을 선택하세요"
                    value={summaryForm.curriculum_id}
                    onChange={(e) => setSummaryForm({ 
                      ...summaryForm, 
                      curriculum_id: e.target.value,
                      week_number: 1 
                    })}
                    color={textColor}
                    borderColor={borderColor}
                  >
                    {curriculums
                      .filter(curriculum => {
                        const currentUserId = getCurrentUserId();
                        // owner_id가 있는 경우에만 비교, 없으면 모든 커리큘럼 표시 (안전장치)
                        return !curriculum.owner_id || curriculum.owner_id === currentUserId;
                      })
                      .map((curriculum) => (
                        <option key={curriculum.id} value={curriculum.id}>
                          📖 {curriculum.title}
                        </option>
                      ))}
                  </Select>
                </FormControl>

                {summaryForm.curriculum_id && (
                  <FormControl isRequired>
                    <FormLabel color={textColor}>📅 주차 선택</FormLabel>
                    <Select
                      value={summaryForm.week_number}
                      onChange={(e) => setSummaryForm({ 
                        ...summaryForm, 
                        week_number: parseInt(e.target.value) 
                      })}
                      color={textColor}
                      borderColor={borderColor}
                    >
                      {(getSelectedCurriculumWeeks() ?? []).map((week) => (
                        <option key={week.week_number} value={week.week_number}>
                          📅 {week.week_number}주차: {week.title ?? `${week.week_number}주차`}
                          ({Array.isArray(week.lessons) ? week.lessons.length : 0}개 레슨)
                        </option>
                      ))}
                    </Select>
                  </FormControl>
                )}

                {/* 선택된 주차의 레슨 정보 표시 */}
                {summaryForm.curriculum_id && summaryForm.week_number && (
                  <Box w="100%" p={3} bg="blue.50" borderRadius="md" borderColor={borderColor}>
                    <Text fontSize="sm" fontWeight="semibold" color="blue.700" mb={2}>
                      📚 {summaryForm.week_number}주차 학습 내용:
                    </Text>
                    <VStack align="start" spacing={1}>
                      {(getSelectedWeekLessons() ?? []).map((lesson, index) => (
                        <Text key={index} fontSize="sm" color="blue.600">
                          📝 {lesson}
                        </Text>
                      )) || null}
                    </VStack>
                  </Box>
                )}

                <FormControl isRequired>
                  <FormLabel color={textColor}>📝 요약 내용</FormLabel>
                  <Textarea
                    placeholder="학습한 내용을 요약해주세요... ✨ (최소 100자)"
                    value={summaryForm.content}
                    onChange={(e) => setSummaryForm({ ...summaryForm, content: e.target.value })}
                    color={textColor}
                    borderColor={borderColor}
                    rows={8}
                    minLength={100}
                  />
                  <Text fontSize="xs" color={secondaryTextColor} mt={1}>
                    📊 {(summaryForm.content?.length ?? 0)}/5000자 (최소 100자 필요)
                  </Text>
                </FormControl>
              </VStack>
            </ModalBody>

            <ModalFooter>
              <Button variant="ghost" mr={3} onClick={onCreateModalClose}>
                ❌ 취소
              </Button>
              <Button 
                colorScheme="blue" 
                onClick={handleCreateSummary}
                isLoading={submitting}
                loadingText="💾 저장 중..."
                isDisabled={(summaryForm.content?.length ?? 0) < 100}
                leftIcon={<Text>💾</Text>}
              >
                저장하기
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>

        {/* 요약 수정 모달 */}
        <Modal isOpen={isEditModalOpen} onClose={onEditModalClose} size="xl">
          <ModalOverlay />
          <ModalContent bg={cardBg} color={textColor}>
            <ModalHeader>✏️ 요약 수정</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <VStack spacing={4}>
                <Box w="100%">
                  <Text fontWeight="semibold" color={textColor} mb={2}>
                    📖 {editingSummary && getCurriculumTitle(editingSummary.curriculum_id)} - 📅 {editingSummary?.week_number}주차
                  </Text>
                </Box>
                
                <FormControl isRequired>
                  <FormLabel color={textColor}>📝 요약 내용</FormLabel>
                  <Textarea
                    value={summaryForm.content}
                    onChange={(e) => setSummaryForm({ ...summaryForm, content: e.target.value })}
                    color={textColor}
                    borderColor={borderColor}
                    rows={8}
                    minLength={100}
                    placeholder="학습한 내용을 요약해주세요... ✨"
                  />
                  <Text fontSize="xs" color={secondaryTextColor} mt={1}>
                    📊 {(summaryForm.content?.length ?? 0)}/5000자 (최소 100자 필요)
                  </Text>
                </FormControl>
              </VStack>
            </ModalBody>
            <ModalFooter>
              <Button variant="ghost" mr={3} onClick={onEditModalClose}>
                ❌ 취소
              </Button>
              <Button 
                colorScheme="blue" 
                onClick={handleUpdateSummary}
                isLoading={submitting}
                loadingText="✏️ 수정 중..."
                isDisabled={(summaryForm.content?.length ?? 0) < 100}
                leftIcon={<Text>✏️</Text>}
              >
                수정하기
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </VStack>
    </Container>
  );
};

export default Summary;
