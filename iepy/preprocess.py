from iepy.models import PreProcessSteps

import logging

logger = logging.getLogger(__name__)


class PreProcessPipeline(object):
    """Coordinates the pre-processing tasks on a set of documents"""

    def __init__(self, step_runners, documents_manager):
        """Takes a list of callables and a documents-manager.

            Step Runners may be any callable. It they have an attribute step,
            then that runner will be treated as the responsible for
            accomplishing such a PreProcessStep.
        """
        self.step_runners = step_runners
        self.documents = documents_manager

    def walk_document(self, doc):
        """Computes all the missing pre-process steps for the given document"""
        for step in self.step_runners():
            step(doc)
        return

    def process_step_in_batch(self, runner):
        """Tries to apply the required step to all documents lacking it"""
        logger.info('Starting preprocessing step %s', runner)
        if hasattr(runner, 'step'):
            docs = self.documents.get_documents_lacking_preprocess(runner.step)
        else:
            docs = self.documents  # everything
        for i, doc in enumerate(docs):
            runner(doc)
            logger.info('\tDone for %i documents', i+1)

    def process_everything(self):
        """Tries to apply all the steps to all documents"""
        for runner in self.step_runners:
            self.process_step_in_batch(runner)


class BasePreProcessStepRunner(object):

    def __init__(self, step):
        if not isinstance(step, PreProcessSteps):
            raise ValueError()
        self.step = step

    def __call__(self, doc):
        # You'll have to:
        # - check if the document satisfies pre-conditions
        # - decide what to do if the document had that sted already done:
        #    - skip?
        #    - re-doit?
        #    - raise?
        # - store pre process results on the document
        raise NotImplementedError


